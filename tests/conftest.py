"""Pytest configuration and fixtures.

This module provides common fixtures and configuration for all tests.
"""

import os
from collections.abc import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from app import create_app, db
from app.users.models import User, UserType


@pytest.fixture
def app() -> Generator[Flask]:
    """Create and configure a new app instance for each test."""
    # Set environment to testing
    os.environ['FLASK_ENV'] = 'testing'

    # Create app with test configuration
    test_app = create_app()

    # Create the database and the database table
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def manager_user_id(app: Flask) -> int:
    """Create a manager user for testing and return its ID."""
    with app.app_context():
        existing_user = User.query.filter_by(email='manager@test.com').first()
        if existing_user:
            return int(existing_user.id)

        user = User()
        user.name = 'Test Manager'
        user.email = 'manager@test.com'
        user.set_password('password123')
        user.user_type = UserType.MANAGER

        db.session.add(user)
        db.session.commit()

        return int(user.id)


@pytest.fixture
def manager_user(app: Flask, manager_user_id: int) -> User | None:
    """Get manager user by ID to avoid DetachedInstanceError."""
    with app.app_context():
        return db.session.get(User, manager_user_id)


@pytest.fixture
def employee_user_id(app: Flask) -> int:
    """Create an employee user for testing and return its ID."""
    with app.app_context():
        existing_user = User.query.filter_by(email='employee@test.com').first()
        if existing_user:
            return int(existing_user.id)

        user = User()
        user.name = 'Test Employee'
        user.email = 'employee@test.com'
        user.set_password('password123')
        user.user_type = UserType.EMPLOYEE

        db.session.add(user)
        db.session.commit()

        return int(user.id)


@pytest.fixture
def employee_user(app: Flask, employee_user_id: int) -> User | None:
    """Get employee user by ID to avoid DetachedInstanceError."""
    with app.app_context():
        return db.session.get(User, employee_user_id)


@pytest.fixture
def auth_headers_manager(
    client: FlaskClient,
    manager_user: User,
) -> dict[str, str]:
    """Create authentication headers for manager user."""
    response = client.post(
        '/auth/login',
        json={
            'email': 'manager@test.com',
            'password': 'password123',
        },
    )

    data = response.get_json()
    token = data['access_token']

    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def auth_headers_employee(
    client: FlaskClient,
    employee_user: User,
) -> dict[str, str]:
    """Create authentication headers for employee user."""
    response = client.post(
        '/auth/login',
        json={
            'email': 'employee@test.com',
            'password': 'password123',
        },
    )

    data = response.get_json()
    token = data['access_token']

    return {'Authorization': f'Bearer {token}'}
