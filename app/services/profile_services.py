from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.profile import ProfileUpdate


def get_profile_service(
    current_user: User
):
    return current_user

def update_profile_service(
    db: Session,
    profile_data: ProfileUpdate,
    current_user: User
):

    update_data = profile_data.model_dump(exclude_unset=True)

     for field, value in update_data.items():
         setattr(current_user, field, value)

     db.commit()
     db.refresh(current_user)

     return current_user