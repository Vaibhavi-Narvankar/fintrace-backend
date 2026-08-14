from fastapi import Depends
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.core.exceptions import ForbiddenException


def require_role(required_role: UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:

        if current_user.role != required_role:
            raise ForbiddenException(
                message="Insufficient permissions"
            )

        return current_user

    return role_checker