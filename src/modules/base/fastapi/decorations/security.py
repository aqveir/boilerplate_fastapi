import functools
from typing import Any, Callable
from fastapi.security import OAuth2PasswordBearer

def permissions(privileges: list[str] = ["*"]):
    """
    Decorator to check permissions for a route.

    Args:
        permission (str): The permission to check.
        permission_type (str): The type of permission to check.
        is_admin_required (bool): Whether admin access is required.

    Returns:
        function: The decorated function.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(privileges=privileges, *args, **kwargs):
            # Check permissions here
            if "*" not in privileges and "all" not in privileges:
                for privilege in privileges:
                    if privilege == "*":
                        # Check for all permissions
                        pass
                    else:
                        # Check for specific permission
                        pass
                token = OAuth2PasswordBearer(tokenUrl="token")
                print(f"Token: {token}")
            else:
                pass

            return func(*args, **kwargs)

        return wrapper

    return decorator


def test_permissions(func: Callable) -> Callable:
    @functools.wraps(func)
    def test_func():
        return func()
    return test_func