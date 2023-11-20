#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Union


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
            hashed_password = user.hashed_password
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Find user by session ID """

        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session. The method updates the corresponding
            user’s session ID to None
        """

        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""

        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(user.id, hashed_password=hashed_password)
                self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError()
