MAX_PROJECT_NAME_LEN = 200
MIN_USER_ID = 1


def _check_is_dict(data: object) -> str | None:
    if not isinstance(data, dict):
        return 'Request body must be JSON'
    return None


def _check_required_fields(
    data: dict[str, object],
    required: tuple[str, ...],
) -> str | None:
    for field in required:
        if field not in data:
            return f"Field '{field}' is required"
    return None


def _check_name(name: object) -> str | None:
    if not isinstance(name, str) or not name.strip():
        return "Field 'name' must be a non-empty string"
    if len(name) > MAX_PROJECT_NAME_LEN:
        return (
            f"Field 'name' must be at most {MAX_PROJECT_NAME_LEN} characters"
        )
    return None


def _check_description(description: object) -> str | None:
    if description is not None and not isinstance(description, str):
        return "Field 'description' must be a string"
    return None


def _check_user_id(user_id: object) -> str | None:
    if not isinstance(user_id, int) or user_id < MIN_USER_ID:
        return "Field 'user_id' must be a positive integer"
    return None


def validate_project_data(
    data: dict[str, object],
    *,
    is_update: bool = False,
) -> tuple[bool, str | None]:
    err = _check_is_dict(data)
    if err:
        return False, err

    if not is_update:
        err = _check_required_fields(data, ('name', 'user_id'))
        if err:
            return False, err

    if 'name' in data:
        err = _check_name(data['name'])
        if err:
            return False, err

    if 'description' in data:
        err = _check_description(data['description'])
        if err:
            return False, err

    if 'user_id' in data:
        err = _check_user_id(data['user_id'])
        if err:
            return False, err

    return True, None
