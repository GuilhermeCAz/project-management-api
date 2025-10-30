"""Tests for authentication endpoints.

This module tests login, registration, token refresh, logout, and verification.
"""

from flask import Flask
from flask.testing import FlaskClient

from app.users.models import User


class TestAuthLogin:
    """Test cases for login endpoint."""

    def test_login_success(
        self,
        client: FlaskClient,
        manager_user: User,
    ) -> None:
        """Test successful login."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'manager@test.com',
                'password': 'password123',
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'manager@test.com'
        assert data['user']['user_type'] == 'manager'

    def test_login_invalid_email(self, client: FlaskClient) -> None:
        """Test login with invalid email."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'invalid@test.com',
                'password': 'password123',
            },
        )

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_invalid_password(
        self,
        client: FlaskClient,
        manager_user: User,
    ) -> None:
        """Test login with invalid password."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'manager@test.com',
                'password': 'wrongpassword',
            },
        )

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_login_missing_data(self, client: FlaskClient) -> None:
        """Test login with missing data."""
        response = client.post(
            '/auth/login',
            json={
                'email': 'manager@test.com',
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_login_invalid_json(self, client: FlaskClient) -> None:
        """Test login with invalid JSON."""
        response = client.post('/auth/login', data='invalid json')

        assert response.status_code == 400


class TestAuthRegister:
    """Test cases for registration endpoint."""

    def test_register_success(self, client: FlaskClient, app: Flask) -> None:
        """Test successful registration."""
        response = client.post(
            '/auth/register',
            json={
                'name': 'New User',
                'email': 'newuser@test.com',
                'password': 'password123',
                'user_type': 'employee',
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['email'] == 'newuser@test.com'
        assert data['user']['user_type'] == 'employee'

    def test_register_duplicate_email(
        self,
        client: FlaskClient,
        manager_user: User,
    ) -> None:
        """Test registration with duplicate email."""
        response = client.post(
            '/auth/register',
            json={
                'name': 'Another User',
                'email': 'manager@test.com',
                'password': 'password123',
                'user_type': 'employee',
            },
        )

        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data

    def test_register_missing_data(self, client: FlaskClient) -> None:
        """Test registration with missing data."""
        response = client.post(
            '/auth/register',
            json={
                'name': 'New User',
                'email': 'newuser@test.com',
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestAuthRefresh:
    """Test cases for token refresh endpoint."""

    def test_refresh_success(
        self,
        client: FlaskClient,
        manager_user: User,
    ) -> None:
        """Test successful token refresh."""
        # First login to get tokens
        login_response = client.post(
            '/auth/login',
            json={
                'email': 'manager@test.com',
                'password': 'password123',
            },
        )

        login_data = login_response.get_json()
        refresh_token = login_data['refresh_token']

        # Use refresh token to get new access token
        response = client.post(
            '/auth/refresh',
            json={
                'refresh_token': refresh_token,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data

    def test_refresh_invalid_token(self, client: FlaskClient) -> None:
        """Test refresh with invalid token."""
        response = client.post(
            '/auth/refresh',
            json={
                'refresh_token': 'invalid_token',
            },
        )

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


class TestAuthLogout:
    """Test cases for logout endpoint."""

    def test_logout_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test successful logout."""
        response = client.post('/auth/logout', headers=auth_headers_manager)

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_logout_no_token(self, client: FlaskClient) -> None:
        """Test logout without token."""
        response = client.post('/auth/logout')

        assert response.status_code == 401


class TestAuthVerify:
    """Test cases for token verification endpoint."""

    def test_verify_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test successful token verification."""
        response = client.get('/auth/verify', headers=auth_headers_manager)

        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data

    def test_verify_no_token(self, client: FlaskClient) -> None:
        """Test verification without token."""
        response = client.get('/auth/verify')

        assert response.status_code == 401

    def test_verify_invalid_token(self, client: FlaskClient) -> None:
        """Test verification with invalid token."""
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.get('/auth/verify', headers=headers)

        assert response.status_code == 401
