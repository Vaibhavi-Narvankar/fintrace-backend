from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.profile import ProfileUpdate


def get_profile_service(
    current_user: User
):
    return current_user

async def update_profile_service(
    db: AsyncSession,
    profile_data: ProfileUpdate,
    current_user: User
):
    update_data = profile_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user