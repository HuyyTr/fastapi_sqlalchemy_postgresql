from fastapi import APIRouter, HTTPException, status, Depends

from schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from services.user import UserService

user_router = APIRouter()


@user_router.get("/{id}", response_model=UserSchema)
async def get_user(id: int, use_service: UserService = Depends(UserService)):
    user = await use_service.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserSchema.model_validate(user)


@user_router.post("/users", response_model=UserSchema)
async def create_user(user_in: UserCreateSchema, use_service: UserService = Depends(UserService)):
    user = await use_service.create(user_in)
    print(f"----22222---->{repr(user)}")
    return user
