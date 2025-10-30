"""Tests for task management endpoints.

This module tests CRUD operations for tasks.
"""

from flask import Flask
from flask.testing import FlaskClient

from app import db
from app.projects.models import Project
from app.tasks.models import Task
from app.users.models import User


class TestTaskCreate:
    """Test cases for task creation endpoint."""

    def test_create_task_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful task creation by manager."""
        # Create a test project first
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.post(
            '/tasks',
            headers=auth_headers_manager,
            json={
                'title': 'New Task',
                'description': 'A test task',
                'status': 'pending',
                'project_id': project_id,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Task'
        assert data['description'] == 'A test task'
        assert data['status'] == 'pending'
        assert data['project_id'] == project_id

    def test_create_task_by_employee(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task creation by employee (should succeed)."""
        # Create a test project first
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.post(
            '/tasks',
            headers=auth_headers_employee,
            json={
                'title': 'Employee Task',
                'description': 'A task by employee',
                'status': 'pending',
                'project_id': project_id,
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Employee Task'

    def test_create_task_missing_data(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task creation with missing data."""
        # Create a test project first
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.post(
            '/tasks',
            headers=auth_headers_manager,
            json={
                'description': 'A test task',
                'status': 'pending',
                'project_id': project_id,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_task_invalid_status(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task creation with invalid status."""
        # Create a test project first
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = client.post(
            '/tasks',
            headers=auth_headers_manager,
            json={
                'title': 'New Task',
                'description': 'A test task',
                'status': 'invalid_status',
                'project_id': project_id,
            },
        )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_task_invalid_project(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test task creation with invalid project_id."""
        response = client.post(
            '/tasks',
            headers=auth_headers_manager,
            json={
                'title': 'New Task',
                'description': 'A test task',
                'status': 'pending',
                'project_id': 999,
            },
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestTaskList:
    """Test cases for task listing endpoint."""

    def test_get_tasks_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful task listing."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()

        response = client.get('/tasks', headers=auth_headers_manager)

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'tasks' in data
        assert 'count' in data
        assert isinstance(data['tasks'], list)
        assert len(data['tasks']) >= 1

    def test_get_tasks_with_filter(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task listing with status filter."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'completed'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()

        response = client.get(
            '/tasks?status=completed',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'tasks' in data
        assert 'count' in data
        assert isinstance(data['tasks'], list)
        for task in data['tasks']:
            assert task['status'] == 'completed'

    def test_get_tasks_with_project_filter(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task listing with project_id filter."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            project_id = project.id

        response = client.get(
            f'/tasks?project_id={project_id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'tasks' in data
        assert 'count' in data
        assert isinstance(data['tasks'], list)
        for task in data['tasks']:
            assert task['project_id'] == project_id

    def test_get_tasks_with_pagination(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task listing with pagination."""
        # Create a test project and multiple tasks
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            for i in range(3):
                task = Task()
                task.title = f'Test Task {i}'
                task.description = f'Test Description {i}'
                task.status = 'pending'
                task.project_id = project.id
                db.session.add(task)
            db.session.commit()

        response = client.get(
            '/tasks?limit=2&offset=0',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
        assert 'tasks' in data
        assert 'count' in data
        assert isinstance(data['tasks'], list)
        assert len(data['tasks']) <= 2


class TestTaskDetail:
    """Test cases for task detail endpoint."""

    def test_get_task_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful task retrieval."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.get(
            f'/tasks/{task_id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == task_id
        assert data['title'] == 'Test Task'

    def test_get_task_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test task retrieval with non-existent ID."""
        response = client.get('/tasks/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestTaskUpdate:
    """Test cases for task update endpoint."""

    def test_update_task_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful task update by manager."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            task_id = task.id
            project_id = project.id

        response = client.put(
            f'/tasks/{task_id}',
            headers=auth_headers_manager,
            json={
                'title': 'Updated Task',
                'description': 'Updated Description',
                'status': 'in_progress',
                'project_id': project_id,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Task'
        assert data['description'] == 'Updated Description'
        assert data['status'] == 'in_progress'

    def test_update_task_by_employee(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task update by employee (should succeed)."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            task_id = task.id
            project_id = project.id

        response = client.put(
            f'/tasks/{task_id}',
            headers=auth_headers_employee,
            json={
                'title': 'Updated Task',
                'description': 'Updated Description',
                'status': 'in_progress',
                'project_id': project_id,
            },
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Task'

    def test_update_task_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test task update with non-existent ID."""
        response = client.put(
            '/tasks/999',
            headers=auth_headers_manager,
            json={
                'title': 'Updated Task',
                'description': 'Updated Description',
                'status': 'in_progress',
                'project_id': 1,
            },
        )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestTaskDelete:
    """Test cases for task deletion endpoint."""

    def test_delete_task_success(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test successful task deletion by manager."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.delete(
            f'/tasks/{task_id}',
            headers=auth_headers_manager,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_delete_task_by_employee(
        self,
        client: FlaskClient,
        auth_headers_employee: dict[str, str],
        manager_user: User,
    ) -> None:
        """Test task deletion by employee (should succeed)."""
        # Create a test project and task
        with client.application.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id
            db.session.add(task)
            db.session.commit()
            task_id = task.id

        response = client.delete(
            f'/tasks/{task_id}',
            headers=auth_headers_employee,
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data

    def test_delete_task_not_found(
        self,
        client: FlaskClient,
        auth_headers_manager: dict[str, str],
    ) -> None:
        """Test task deletion with non-existent ID."""
        response = client.delete('/tasks/999', headers=auth_headers_manager)

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data


class TestTaskModel:
    """Test cases for Task model."""

    def test_task_creation(self, app: Flask, manager_user: User) -> None:
        """Test task model creation."""
        with app.app_context():
            # Create a project first
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            # Create a task
            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id

            db.session.add(task)
            db.session.commit()

            assert task.id is not None
            assert task.title == 'Test Task'
            assert task.description == 'Test Description'
            assert task.status == 'pending'
            assert task.project_id == project.id

    def test_task_to_dict(self, app: Flask, manager_user: User) -> None:
        """Test task to_dict method."""
        with app.app_context():
            # Create a project first
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            # Create a task
            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id

            db.session.add(task)
            db.session.commit()

            task_dict = task.to_dict()

            assert task_dict['title'] == 'Test Task'
            assert task_dict['description'] == 'Test Description'
            assert task_dict['status'] == 'pending'
            assert task_dict['project_id'] == project.id
            assert 'id' in task_dict
            assert 'created_at' in task_dict
            assert 'updated_at' in task_dict

    def test_task_project_relationship(
        self,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test task-project relationship."""
        with app.app_context():
            # Create a project first
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            # Create a task
            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id

            db.session.add(task)
            db.session.commit()

            # Test relationship
            assert task.project.id == project.id
            assert task.project.name == project.name

    def test_task_valid_statuses(self, app: Flask, manager_user: User) -> None:
        """Test task valid statuses."""
        with app.app_context():
            # Create a project first
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            # Test all valid statuses
            valid_statuses = ['pending', 'in_progress', 'completed']

            for status in valid_statuses:
                task = Task()
                task.title = f'Test Task {status}'
                task.description = 'Test Description'
                task.status = status
                task.project_id = project.id

                db.session.add(task)
                db.session.commit()

                assert task.status == status
