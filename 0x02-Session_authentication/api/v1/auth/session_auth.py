#!/usr/bin/env python3
""" Session auth module """
from api.v1.auth.auth import Auth
from flask import request
import uuid
from typing import TypeVar


class SessionAuth(Auth):
    """Session auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Function that  that creates a Session ID for a user_id """

        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())

        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Function that returns a User ID based on a Session ID"""

        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        User_id = SessionAuth.user_id_by_session_id.get(session_id)
        return User_id

    def current_user(self, request=None) -> TypeVar('User'):
        """Function that returns a User instance based on a cookie value"""
        from models.user import User

        cookie_val = self.session_cookie(request)
        if cookie_val is None:
            return None
        id_user = self.user_id_for_session_id(cookie_val)
        if id_user is None:
            return None
        user = User.get(id_user)

        return user
