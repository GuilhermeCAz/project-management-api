"""
User model definition.

This module defines the User model and related enums.
"""

from datetime import UTC, datetime
from enum import Enum

from app import db


class UserType(Enum):
    """Enumeration for user types in the system."""

    MANAGER = 'manager'
    EMPLOYEE = 'employee'


class User(db.Model):  # type: ignore[name-defined, misc]
    """
    User model representing system users.

    A user can be either a manager or an employee. Managers have
    additional privileges to modify database records.

    Attributes:
        id (int): Primary key
        name (str): User's full name
        email (str): User's email address (unique)
        user_type (UserType): Type of user (manager or employee)
        created_at (datetime): Timestamp of user creation
        updated_at (datetime): Timestamp of last update

    Relationships:
        projects (list[Project]): Projects owned by this user
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    user_type = db.Column(
        db.Enum(UserType),
        nullable=False,
        default=UserType.EMPLOYEE,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(UTC),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    projects = db.relationship(
        'Project',
        backref='owner',
        lazy='dynamic',
        cascade='all, delete-orphan',
    )

    def to_dict(self, *, include_projects: bool = False) -> dict[str, object]:
        """
        Convert user object to dictionary representation.

        Args:
            include_projects (bool): Whether to include user's projects

        Returns:
            dict: Dictionary representation of the user
        """
        result = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'user_type': self.user_type.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

        if include_projects:
            result['projects'] = [
                project.to_dict() for project in self.projects.all()
            ]

        return result

    def __repr__(self) -> str:
        """String representation of User."""
        return f'<User {self.name} ({self.user_type.value})>'
