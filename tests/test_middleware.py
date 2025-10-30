"""Tests for authentication middleware.

This module tests JWT token validation and authentication middleware.
"""

from datetime import UTC, datetime, timedelta

import jwt
from flask import Flask
from flask.testing import FlaskClient

from app.users.models import User


class TestJWTMiddleware:
    """Test cases for JWT authentication middleware."""

    def test_valid_token_access(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test access with valid JWT token."""
        response = client.get('/users', headers=auth_headers_manager)
        assert response.status_code == 200

    def test_missing_token(self, client: FlaskClient) -> None:
        """Test access without JWT token."""
        response = client.get('/users')
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'authorization' in data['error'].lower()

    def test_invalid_token_format(self, client: FlaskClient) -> None:
        """Test access with invalid token format."""
        headers = {'Authorization': 'InvalidToken'}
        response = client.get('/users', headers=headers)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_malformed_bearer_token(self, client: FlaskClient) -> None:
        """Test access with malformed Bearer token."""
        headers = {'Authorization': 'Bearer'}
        response = client.get('/users', headers=headers)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_invalid_jwt_token(self, client: FlaskClient) -> None:
        """Test access with invalid JWT token."""
        headers = {'Authorization': 'Bearer invalid.jwt.token'}
        response = client.get('/users', headers=headers)
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_expired_token(
        self,
        client: FlaskClient,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test access with expired JWT token."""
        with app.app_context():
            # Create an expired token
            payload = {
                'user_id': manager_user.id,
                'user_type': manager_user.user_type.value,
                'exp': datetime.now(UTC)
                - timedelta(hours=1),  # Expired 1 hour ago
                'iat': datetime.now(UTC) - timedelta(hours=2),
                'type': 'access',
            }

            expired_token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256',
            )

            headers = {'Authorization': f'Bearer {expired_token}'}
            response = client.get('/users', headers=headers)

            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data
            assert 'expired' in data['error'].lower()

    def test_token_with_invalid_user(
        self,
        client: FlaskClient,
        app: Flask,
    ) -> None:
        """Test access with token for non-existent user."""
        with app.app_context():
            # Create a token for non-existent user
            payload = {
                'user_id': 999,  # Non-existent user
                'user_type': 'manager',
                'exp': datetime.now(UTC) + timedelta(hours=1),
                'iat': datetime.now(UTC),
                'type': 'access',
            }

            invalid_user_token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256',
            )

            headers = {'Authorization': f'Bearer {invalid_user_token}'}
            response = client.get('/users', headers=headers)

            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data

    def test_refresh_token_for_access(
        self,
        client: FlaskClient,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test using refresh token for access (should fail)."""
        with app.app_context():
            # Create a refresh token
            payload = {
                'user_id': manager_user.id,
                'user_type': manager_user.user_type.value,
                'exp': datetime.now(UTC) + timedelta(days=7),
                'iat': datetime.now(UTC),
                'type': 'refresh',  # This is a refresh token, not access
            }

            refresh_token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256',
            )

            headers = {'Authorization': f'Bearer {refresh_token}'}
            response = client.get('/users', headers=headers)

            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data

    def test_token_without_required_fields(
        self,
        client: FlaskClient,
        app: Flask,
    ) -> None:
        """Test token missing required fields."""
        with app.app_context():
            # Create a token without user_id
            payload = {
                'user_type': 'manager',
                'exp': datetime.now(UTC) + timedelta(hours=1),
                'iat': datetime.now(UTC),
                'type': 'access',
            }

            incomplete_token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256',
            )

            headers = {'Authorization': f'Bearer {incomplete_token}'}
            response = client.get('/users', headers=headers)

            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data

    def test_token_with_wrong_secret(
        self,
        client: FlaskClient,
        manager_user: User,
    ) -> None:
        """Test token signed with wrong secret."""
        # Create a token with wrong secret
        payload = {
            'user_id': manager_user.id,
            'user_type': manager_user.user_type.value,
            'exp': datetime.now(UTC) + timedelta(hours=1),
            'iat': datetime.now(UTC),
            'type': 'access',
        }

        wrong_secret_token = jwt.encode(
            payload,
            'wrong_secret_key',  # Wrong secret
            algorithm='HS256',
        )

        headers = {'Authorization': f'Bearer {wrong_secret_token}'}
        response = client.get('/users', headers=headers)

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


class TestAuthorizationMiddleware:
    """Test cases for authorization middleware."""

    def test_manager_access_to_user_endpoints(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test that managers can access user management endpoints."""
        # Test GET users
        response = client.get('/users', headers=auth_headers_manager)
        assert response.status_code == 200

        # Test POST users
        response = client.post(
            '/users',
            headers=auth_headers_manager,
            json={
                'name': 'New User',
                'email': 'newuser@test.com',
                'user_type': 'employee',
                'user_id': 1,
            },
        )
        assert response.status_code == 201

    def test_employee_denied_user_management(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
    ) -> None:
        """Test that employees cannot access user management endpoints."""
        # Test POST users (should fail)
        response = client.post(
            '/users',
            headers=auth_headers_employee,
            json={
                'name': 'New User',
                'email': 'newuser@test.com',
                'user_type': 'employee',
                'user_id': 2,
            },
        )
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_manager_access_to_project_endpoints(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test that managers can access project management endpoints."""
        # Test GET projects
        response = client.get('/projects', headers=auth_headers_manager)
        assert response.status_code == 200

        # Test POST projects
        response = client.post(
            '/projects',
            headers=auth_headers_manager,
            json={
                'name': 'New Project',
                'description': 'Test project',
                'user_id': 1,
            },
        )
        assert response.status_code == 201

    def test_employee_denied_project_management(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
    ) -> None:
        """Test that employees cannot create/update/delete projects."""
        # Test POST projects (should fail)
        response = client.post(
            '/projects',
            headers=auth_headers_employee,
            json={
                'name': 'New Project',
                'description': 'Test project',
                'user_id': 2,
            },
        )
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_both_users_access_tasks(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        auth_headers_employee: dict[str, str],
    ) -> None:
        """Test that both managers and employees can access task endpoints."""
        # Test manager access
        response = client.get('/tasks', headers=auth_headers_manager)
        assert response.status_code == 200

        # Test employee access
        response = client.get('/tasks', headers=auth_headers_employee)
        assert response.status_code == 200

    def test_public_auth_endpoints(self, client: FlaskClient) -> None:
        """Test that authentication endpoints are publicly accessible."""
        # Test login endpoint
        response = client.post(
            '/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'password123',
            },
        )
        # Should return 401 for invalid credentials, not 403 for access denied
        assert response.status_code in [400, 401]

        # Test register endpoint
        response = client.post(
            '/auth/register',
            json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'password123',
                'user_type': 'employee',
            },
        )
        assert response.status_code != 403
