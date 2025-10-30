"""Tests for user management endpoints.

This module tests CRUD operations for users.
"""

import time

from flask import Flask
from flask.testing import FlaskClient

from app import db
from app.users.models import User, UserType


class TestUserCreate:
    """Test cases for user creation endpoint."""

    def test_create_user_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test successful user creation by manager."""
        unique_email = f'newemployee{int(time.time())}@test.com'

        response = client.post(
            '/users',
            headers=auth_headers_manager,
            json={
                'name': 'New Employee',
                'email': unique_email,
                'user_type': 'employee',
                'user_id': 1,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'New Employee'
        assert data['email'] == unique_email
        assert data['user_type'] == 'employee'

    def test_create_user_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
    ) -> None:
        """Test user creation by employee (should fail)."""
        response = client.post(
            '/users',
            headers=auth_headers_employee,
            json={
                'name': 'New Employee',
                'email': 'newemployee@test.com',
                'user_type': 'employee',
                'user_id': 2,
            },
        )

        assert response.status_code == 403

    def test_create_user_duplicate_email(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        employee_user: User,
    ) -> None:
        """Test user creation with duplicate email."""
        response = client.post(
            '/users',
            headers=auth_headers_manager,
            json={
                'name': 'Another Employee',
                'email': 'employee@test.com',
                'user_type': 'employee',
                'user_id': 1,
            },
        )

        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data

    def test_create_user_missing_data(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test user creation with missing data."""
        response = client.post(
            '/users',
            headers=auth_headers_manager,
            json={
                'name': 'New Employee',
                'user_type': 'employee',
                'user_id': 1,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestUserList:
    """Test cases for user listing endpoint."""

    def test_get_users_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
        employee_user: User,
    ) -> None:
        """Test successful user listing."""
        response = client.get('/users', headers=auth_headers_manager)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'users' in data
        assert 'count' in data
        assert isinstance(data['users'], list)
        assert len(data['users']) >= 2  # At least manager and employee
        assert data['count'] >= 2

    def test_get_users_with_filter(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
        employee_user: User,
    ) -> None:
        """Test user listing with user_type filter."""
        response = client.get(
            '/users?user_type=manager',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'users' in data
        assert 'count' in data
        assert isinstance(data['users'], list)
        for user in data['users']:
            assert user['user_type'] == 'manager'

    def test_get_users_with_pagination(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
        employee_user: User,
    ) -> None:
        """Test user listing with pagination."""
        response = client.get(
            '/users?limit=1&offset=0',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'users' in data
        assert 'count' in data
        assert isinstance(data['users'], list)
        assert len(data['users']) <= 1

    def test_get_users_invalid_filter(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test user listing with invalid filter."""
        response = client.get(
            '/users?user_type=invalid',
            headers=auth_headers_manager,
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestUserDetail:
    """Test cases for user detail endpoint."""

    def test_get_user_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        employee_user: User,
    ) -> None:
        """Test successful user retrieval."""
        response = client.get(
            f'/users/{employee_user.id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == employee_user.id
        assert data['email'] == employee_user.email

    def test_get_user_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test user retrieval with non-existent ID."""
        response = client.get('/users/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestUserUpdate:
    """Test cases for user update endpoint."""

    def test_update_user_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        employee_user: User,
    ) -> None:
        """Test successful user update by manager."""
        response = client.put(
            f'/users/{employee_user.id}',
            headers=auth_headers_manager,
            json={
                'name': 'Updated Employee',
                'email': 'updated@test.com',
                'user_type': 'manager',
                'user_id': 1,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Employee'
        assert data['email'] == 'updated@test.com'
        assert data['user_type'] == 'manager'

    def test_update_user_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test user update by employee (should fail)."""
        response = client.put(
            f'/users/{manager_user.id}',
            headers=auth_headers_employee,
            json={
                'name': 'Updated Manager',
                'email': 'updated@test.com',
                'user_type': 'manager',
                'user_id': 2,
            },
        )

        assert response.status_code == 403

    def test_update_user_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test user update with non-existent ID."""
        response = client.put(
            '/users/999',
            headers=auth_headers_manager,
            json={
                'name': 'Updated User',
                'email': 'updated@test.com',
                'user_type': 'employee',
                'user_id': 1,
            },
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestUserDelete:
    """Test cases for user deletion endpoint."""

    def test_delete_user_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        employee_user: User,
    ) -> None:
        """Test successful user deletion by manager."""
        response = client.delete(
            f'/users/{employee_user.id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_delete_user_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test user deletion by employee (should fail)."""
        response = client.delete(
            f'/users/{manager_user.id}',
            headers=auth_headers_employee,
        )

        assert response.status_code == 403

    def test_delete_user_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test user deletion with non-existent ID."""
        response = client.delete('/users/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestUserModel:
    """Test cases for User model."""

    def test_user_creation(self, app: Flask) -> None:
        """Test user model creation."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.EMPLOYEE

            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.name == 'Test User'
            assert user.email == 'test@example.com'
            assert user.user_type == UserType.EMPLOYEE

    def test_password_hashing(self, app: Flask) -> None:
        """Test password hashing and verification."""
        with app.app_context():
            user = User()
            user.set_password('password123')

            assert user.check_password('password123') is True
            assert user.check_password('wrongpassword') is False

    def test_user_to_dict(self, app: Flask) -> None:
        """Test user to_dict method."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.EMPLOYEE

            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()

            assert user_dict['name'] == 'Test User'
            assert user_dict['email'] == 'test@example.com'
            assert user_dict['user_type'] == 'employee'
            assert 'id' in user_dict
            assert 'created_at' in user_dict
            assert 'updated_at' in user_dict
