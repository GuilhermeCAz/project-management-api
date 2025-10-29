"""
Authentication and authorization middleware.

This module provides decorators for route protection based on user roles.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import jsonify, request

from app import db


def manager_required(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to require manager role for accessing a route.

    This decorator checks if the user_id in the request corresponds
    to a manager user. Routes that affect the database should be
    protected with this decorator.

    The user_id can be provided via:
    - Request JSON body: {'user_id': 1}
    - Query parameter: ?user_id=1
    - HTTP Header: X-User-Id: 1

    Args:
        f (function): The route function to decorate

    Returns:
        function: The decorated function

    Raises:
        400: If user_id is not provided or invalid
        403: If user is not a manager
        404: If user is not found

    Example:
        >>> @app.route('/projects', methods=['POST'])
        >>> @manager_required
        >>> def create_project():
        >>>     # Only managers can access this
        >>>     pass
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        from app.users.models import User, UserType  # noqa: PLC0415

        user_id = get_current_user_id()

        if not user_id:
            return jsonify(
                {'error': 'user_id is required for this operation'},
            ), 400

        # Verify user exists and is a manager
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.user_type != UserType.MANAGER:
            return jsonify(
                {
                    'error': 'Access denied. Manager role required.',
                    'user_type': user.user_type.value,
                },
            ), 403

        return f(*args, **kwargs)

    return decorated_function


def get_current_user_id() -> int | None:
    """
    Extract user_id from the current request.

    Checks multiple sources in order:
    1. JSON body
    2. Query parameters
    3. HTTP headers

    Returns:
        int: The user ID from the request, or None if not found

    Example:
        >>> user_id = get_current_user_id()
        >>> if user_id:
        >>>     user = User.query.get(user_id)
    """
    user_id = None

    if request.is_json and request.json:
        user_id = request.json.get('user_id')

    if not user_id:
        user_id = request.args.get('user_id')

    if not user_id:
        user_id = request.headers.get('X-User-Id')

    if user_id:
        try:
            return int(user_id)
        except (ValueError, TypeError):
            return None

    return None
