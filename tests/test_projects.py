"""Tests for project management endpoints.

This module tests CRUD operations for projects.
"""

from flask import Flask
from flask.testing import FlaskClient

from app import db
from app.projects.models import Project
from app.users.models import User


class TestProjectCreate:
    """Test cases for project creation endpoint."""

    def test_create_project_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test successful project creation by manager."""
        response = client.post(
            '/projects',
            headers=auth_headers_manager,
            json={
                'name': 'New Project',
                'description': 'A test project',
                'user_id': 1,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'New Project'
        assert data['description'] == 'A test project'
        assert data['user_id'] == 1

    def test_create_project_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
    ) -> None:
        """Test project creation by employee (should fail)."""
        response = client.post(
            '/projects',
            headers=auth_headers_employee,
            json={
                'name': 'New Project',
                'description': 'A test project',
                'user_id': 2,
            },
        )

        assert response.status_code == 403

    def test_create_project_missing_data(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test project creation with missing data."""
        response = client.post(
            '/projects',
            headers=auth_headers_manager,
            json={
                'description': 'A test project',
                'user_id': 1,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_project_invalid_user(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test project creation with invalid user_id."""
        response = client.post(
            '/projects',
            headers=auth_headers_manager,
            json={
                'name': 'New Project',
                'description': 'A test project',
                'user_id': 999,
            },
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestProjectList:
    """Test cases for project listing endpoint."""

    def test_get_projects_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful project listing."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

        response = client.get('/projects', headers=auth_headers_manager)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'projects' in data
        assert 'count' in data
        assert isinstance(data['projects'], list)
        assert len(data['projects']) >= 1

    def test_get_projects_with_filter(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test project listing with user_id filter."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

        response = client.get(
            f'/projects?user_id={manager_user.id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'projects' in data
        assert 'count' in data
        assert isinstance(data['projects'], list)
        for project in data['projects']:
            assert project['user_id'] == manager_user.id

    def test_get_projects_with_pagination(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test project listing with pagination."""
        # Create test projects
        with client.application.app_context():
            for i in range(3):
                project = Project()
                project.name = f'Test Project {i}'
                project.description = f'Test Description {i}'
                project.user_id = manager_user.id
                db.session.add(project)
            db.session.commit()

        response = client.get(
            '/projects?limit=2&offset=0',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'projects' in data
        assert 'count' in data
        assert isinstance(data['projects'], list)
        assert len(data['projects']) <= 2


class TestProjectDetail:
    """Test cases for project detail endpoint."""

    def test_get_project_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful project retrieval."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.get(
            f'/projects/{project_id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == project_id
        assert data['name'] == 'Test Project'

    def test_get_project_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test project retrieval with non-existent ID."""
        response = client.get('/projects/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestProjectUpdate:
    """Test cases for project update endpoint."""

    def test_update_project_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful project update by manager."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.put(
            f'/projects/{project_id}',
            headers=auth_headers_manager,
            json={
                'name': 'Updated Project',
                'description': 'Updated Description',
                'user_id': manager_user.id,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Project'
        assert data['description'] == 'Updated Description'

    def test_update_project_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test project update by employee (should fail)."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.put(
            f'/projects/{project_id}',
            headers=auth_headers_employee,
            json={
                'name': 'Updated Project',
                'description': 'Updated Description',
                'user_id': manager_user.id,
            },
        )

        assert response.status_code == 403

    def test_update_project_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test project update with non-existent ID."""
        response = client.put(
            '/projects/999',
            headers=auth_headers_manager,
            json={
                'name': 'Updated Project',
                'description': 'Updated Description',
                'user_id': 1,
            },
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestProjectDelete:
    """Test cases for project deletion endpoint."""

    def test_delete_project_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful project deletion by manager."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.delete(
            f'/projects/{project_id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_delete_project_unauthorized(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test project deletion by employee (should fail)."""
        # Create a test project
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.delete(
            f'/projects/{project_id}',
            headers=auth_headers_employee,
        )

        assert response.status_code == 403

    def test_delete_project_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test project deletion with non-existent ID."""
        response = client.delete('/projects/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestProjectModel:
    """Test cases for Project model."""

    def test_project_creation(self, app: Flask, manager_user: User) -> None:
        """Test project model creation."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            db.session.add(project)
            db.session.commit()

            assert project.id is not None
            assert project.name == 'Test Project'
            assert project.description == 'Test Description'
            assert project.user_id == manager_user.id

    def test_project_to_dict(self, app: Flask, manager_user: User) -> None:
        """Test project to_dict method."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            db.session.add(project)
            db.session.commit()

            project_dict = project.to_dict()

            assert project_dict['name'] == 'Test Project'
            assert project_dict['description'] == 'Test Description'
            assert project_dict['user_id'] == manager_user.id
            assert 'id' in project_dict
            assert 'created_at' in project_dict
            assert 'updated_at' in project_dict

    def test_project_user_relationship(
        self,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test project-user relationship."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            db.session.add(project)
            db.session.commit()

            # Test relationship
            assert project.owner.id == manager_user.id
            assert project.owner.name == manager_user.name
