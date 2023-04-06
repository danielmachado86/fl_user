import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from api import AsyncIOMotorClient, get_database
from pymongo.errors import DuplicateKeyError

from api.models.user import UserCreate, UserUpdate, UserOut, UserInDB
from api.utils import get_password_hash, generate_jwt, verify_password
from api import logging


logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/users")
async def get_users_list():
    logging.info("Trying to get user list...")
    return {"Hello": "World"}


@router.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate, db: AsyncIOMotorClient = Depends(get_database)):  # type: ignore
    try:
        logging.info("Trying to create user {user}...")
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["hashed_password"] = hashed_password
        user_dict["_id"] = str(ObjectId())
        await db.users.insert_one(user_dict)
        return UserOut(**user_dict)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: str, db: AsyncIOMotorClient = Depends(get_database)):  # type: ignore
    logging.info("Trying to find user {user_id}...")
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: str, user: UserUpdate, db: AsyncIOMotorClient = Depends(get_database)  # type: ignore
):
    user_data = user.dict(exclude_unset=True)
    if user_data.get("password"):
        hashed_password = get_password_hash(user_data["password"])
        user_data["hashed_password"] = hashed_password
        del user_data["password"]
    result = await db.users.update_one({"_id": user_id}, {"$set": user_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user_data)


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: AsyncIOMotorClient = Depends(get_database)):  # type: ignore
    result = await db.users.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.post("/users/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorClient = Depends(get_database),  # type: ignore
):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = generate_jwt(user["email"])
    return {"access_token": access_token, "token_type": "bearer"}
