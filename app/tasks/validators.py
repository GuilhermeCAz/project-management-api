from app.tasks.models import Task

MAX_TASK_TITLE_LEN = 200


def _check_is_dict(data: object) -> str | None:
    if not isinstance(data, dict):
        return 'Request body must be JSON'
    return None


def _check_required_title(
    data: dict[str, object],
    *,
    is_update: bool,
) -> str | None:
    if not is_update and 'title' not in data:
        return "Field 'title' is required"
    return None


def _check_title(title: object) -> str | None:
    if not isinstance(title, str) or not title.strip():
        return "Field 'title' must be a non-empty string"
    if len(title) > MAX_TASK_TITLE_LEN:
        return f"Field 'title' must be at most {MAX_TASK_TITLE_LEN} characters"
    return None


def _check_description(description: object) -> str | None:
    if description is not None and not isinstance(description, str):
        return "Field 'description' must be a string"
    return None


def _check_status(status: object) -> str | None:
    if status not in Task.VALID_STATUSES:
        return (
            f"Field 'status' must be one of: {', '.join(Task.VALID_STATUSES)}"
        )
    return None


def validate_task_data(
    data: dict[str, object],
    *,
    is_update: bool = False,
) -> tuple[bool, str | None]:
    err = _check_is_dict(data)
    if err:
        return False, err

    err = _check_required_title(data, is_update=is_update)
    if err:
        return False, err

    if 'title' in data:
        err = _check_title(data['title'])
        if err:
            return False, err

    if 'description' in data:
        err = _check_description(data['description'])
        if err:
            return False, err

    if 'status' in data:
        err = _check_status(data['status'])
        if err:
            return False, err

    return True, None
