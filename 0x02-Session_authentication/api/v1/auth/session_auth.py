#!/usr/bin/env python3
""" Session auth module """
from api.v1.auth.auth import Auth
import uuid


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
