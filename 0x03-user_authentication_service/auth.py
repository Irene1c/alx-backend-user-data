#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ function to Hash a password"""

    psswd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(psswd, salt)
    return hashed_passwd


def _generate_uuid() -> str:
    """Generate UUIDs"""

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to create new user"""

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""

        try:
            user = self._db.find_user_by(email=email)
            hashed_password = _hash_password(password)
            passwd = password.encode('utf-8')
            return bcrypt.checkpw(passwd, hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Get session ID """

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return
