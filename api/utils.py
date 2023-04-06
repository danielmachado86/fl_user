from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from passlib.context import CryptContext
from jose import jwt


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT authentication
JWT_SECRET_KEY = "mysecretkey"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 30


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password using bcrypt
    """
    return pwd_context.verify(password, hashed_password)


def generate_jwt(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generate a JSON Web Token (JWT) with the specified data and expiration time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize MongoDB document to JSON-compatible format
    """
    doc["_id"] = str(doc["_id"])
    return doc


def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Serialize list of MongoDB documents to JSON-compatible format
    """
    return [serialize_doc(doc) for doc in docs]


def get_object_id(id: str) -> ObjectId:
    """
    Convert string ID to MongoDB ObjectId
    """
    return ObjectId(id)
