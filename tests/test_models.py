"""Additional tests for application models.

This module tests model relationships, validations, and edge cases.
"""

from datetime import datetime

import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError

from app import db
from app.projects.models import Project
from app.tasks.models import Task
from app.users.models import User, UserType


class TestUserModel:
    """Additional tests for User model."""

    def test_user_repr(self, app: Flask) -> None:
        """Test user __repr__ method."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.EMPLOYEE

            db.session.add(user)
            db.session.commit()

            repr_str = repr(user)
            assert 'Test User' in repr_str
            assert 'employee' in repr_str

    def test_user_unique_email_constraint(self, app: Flask) -> None:
        """Test that email must be unique."""
        with app.app_context():
            # Create first user
            user1 = User()
            user1.name = 'User 1'
            user1.email = 'test@example.com'
            user1.set_password('password123')
            user1.user_type = UserType.EMPLOYEE

            db.session.add(user1)
            db.session.commit()

            # Try to create second user with same email
            user2 = User()
            user2.name = 'User 2'
            user2.email = 'test@example.com'
            user2.set_password('password456')
            user2.user_type = UserType.MANAGER

            db.session.add(user2)

            with pytest.raises(IntegrityError):
                db.session.commit()

    def test_user_timestamps(self, app: Flask) -> None:
        """Test that timestamps are set correctly."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.EMPLOYEE

            # Before saving
            assert user.created_at is None
            assert user.updated_at is None

            db.session.add(user)
            db.session.commit()

            # After saving
            assert user.created_at is not None
            assert user.updated_at is not None
            assert isinstance(user.created_at, datetime)
            assert isinstance(user.updated_at, datetime)

    def test_user_projects_relationship(self, app: Flask) -> None:
        """Test user-projects relationship."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.MANAGER

            db.session.add(user)
            db.session.commit()

            # Create projects for the user
            project1 = Project()
            project1.name = 'Project 1'
            project1.description = 'Description 1'
            project1.user_id = user.id

            project2 = Project()
            project2.name = 'Project 2'
            project2.description = 'Description 2'
            project2.user_id = user.id

            db.session.add_all([project1, project2])
            db.session.commit()

            # Test relationship
            assert user.projects.count() == 2
            projects_list = user.projects.all()
            assert project1 in projects_list
            assert project2 in projects_list


class TestProjectModel:
    """Additional tests for Project model."""

    def test_project_repr(self, app: Flask, manager_user: User) -> None:
        """Test project __repr__ method."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            db.session.add(project)
            db.session.commit()

            repr_str = repr(project)
            assert 'Test Project' in repr_str

    def test_project_timestamps(self, app: Flask, manager_user: User) -> None:
        """Test that timestamps are set correctly."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            # Before saving
            assert project.created_at is None
            assert project.updated_at is None

            db.session.add(project)
            db.session.commit()

            # After saving
            assert project.created_at is not None
            assert project.updated_at is not None
            assert isinstance(project.created_at, datetime)
            assert isinstance(project.updated_at, datetime)

    def test_project_tasks_relationship(
        self,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test project-tasks relationship."""
        with app.app_context():
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id

            db.session.add(project)
            db.session.commit()

            # Create tasks for the project
            task1 = Task()
            task1.title = 'Task 1'
            task1.description = 'Description 1'
            task1.status = 'pending'
            task1.project_id = project.id

            task2 = Task()
            task2.title = 'Task 2'
            task2.description = 'Description 2'
            task2.status = 'in_progress'
            task2.project_id = project.id

            db.session.add_all([task1, task2])
            db.session.commit()

            # Test relationship
            assert project.tasks.count() == 2
            tasks_list = project.tasks.all()
            assert task1 in tasks_list
            assert task2 in tasks_list

    def test_project_foreign_key_constraint(self, app: Flask) -> None:
        """Test that project can be created with valid user_id."""
        with app.app_context():
            # Create a valid user first
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.MANAGER
            db.session.add(user)
            db.session.commit()

            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = user.id

            db.session.add(project)
            db.session.commit()

            assert project.id is not None
            assert project.user_id == user.id


class TestTaskModel:
    """Additional tests for Task model."""

    def test_task_repr(self, app: Flask, manager_user: User) -> None:
        """Test task __repr__ method."""
        with app.app_context():
            # Create a project first
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

            repr_str = repr(task)
            assert 'Test Task' in repr_str
            assert 'pending' in repr_str

    def test_task_timestamps(self, app: Flask, manager_user: User) -> None:
        """Test that timestamps are set correctly."""
        with app.app_context():
            # Create a project first
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

            # Before saving
            assert task.created_at is None
            assert task.updated_at is None

            db.session.add(task)
            db.session.commit()

            # After saving
            assert task.created_at is not None
            assert task.updated_at is not None
            assert isinstance(task.created_at, datetime)
            assert isinstance(task.updated_at, datetime)

    def test_task_foreign_key_constraint(self, app: Flask) -> None:
        """Test that task can be created with valid project_id."""
        with app.app_context():
            # Create a valid user and project first
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.MANAGER
            db.session.add(user)
            db.session.commit()

            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = user.id
            db.session.add(project)
            db.session.commit()

            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id

            db.session.add(task)
            db.session.commit()

            assert task.id is not None
            assert task.project_id == project.id

    def test_task_status_validation(
        self,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test task status validation."""
        with app.app_context():
            # Create a project first
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = manager_user.id
            db.session.add(project)
            db.session.commit()

            # Test valid statuses
            valid_statuses = Task.VALID_STATUSES
            for status in valid_statuses:
                task = Task()
                task.title = f'Test Task {status}'
                task.description = 'Test Description'
                task.status = status
                task.project_id = project.id

                db.session.add(task)
                db.session.commit()

                assert task.status == status

                # Clean up for next iteration
                db.session.delete(task)
                db.session.commit()


class TestModelRelationships:
    """Test complex model relationships."""

    def test_cascade_delete_user_projects(self, app: Flask) -> None:
        """Test that deleting a user cascades to projects."""
        with app.app_context():
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.MANAGER

            db.session.add(user)
            db.session.commit()

            # Create a project
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = user.id

            db.session.add(project)
            db.session.commit()
            project_id = project.id

            # Delete the user
            db.session.delete(user)
            db.session.commit()

            # Check that project was deleted due to cascade
            remaining_project = db.session.get(Project, project_id)
            assert remaining_project is None

    def test_cascade_delete_project_tasks(
        self,
        app: Flask,
        manager_user: User,
    ) -> None:
        """Test that deleting a project cascades to tasks."""
        with app.app_context():
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
            task_id = task.id

            # Delete the project
            db.session.delete(project)
            db.session.commit()

            # Check that task was deleted due to cascade
            remaining_task = db.session.get(Task, task_id)
            assert remaining_task is None

    def test_full_relationship_chain(self, app: Flask) -> None:
        """Test the full user -> project -> task relationship chain."""
        with app.app_context():
            # Create user
            user = User()
            user.name = 'Test User'
            user.email = 'test@example.com'
            user.set_password('password123')
            user.user_type = UserType.MANAGER

            db.session.add(user)
            db.session.commit()

            # Create project
            project = Project()
            project.name = 'Test Project'
            project.description = 'Test Description'
            project.user_id = user.id

            db.session.add(project)
            db.session.commit()

            # Create task
            task = Task()
            task.title = 'Test Task'
            task.description = 'Test Description'
            task.status = 'pending'
            task.project_id = project.id

            db.session.add(task)
            db.session.commit()

            # Test full chain
            assert task.project.id == project.id
            assert task.project.owner.id == user.id
            assert project.owner.id == user.id
            assert task in project.tasks.all()
            assert project in user.projects.all()
