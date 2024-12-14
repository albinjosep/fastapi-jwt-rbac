from mongoengine import Document, StringField, DateTimeField
from passlib.context import CryptContext
from datetime import datetime

# Password hashing with PassLib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    username = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    role = StringField(default="user")  # default role is 'user'

    # Method to hash password
    def hash_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    # Method to verify password
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

class Project(Document):
    name = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
