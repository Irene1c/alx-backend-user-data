#!/usr/bin/env python3
"""Session Expiration """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ session expiration """

    def __init__(self):
        """class constructor"""
        session_duration = getenv('SESSION_DURATION')

        try:
            if session_duration:
                self.session_duration = int(session_duration)
            else:
                self.session_duration = 0
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID"""

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        SessionAuth.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID based on a Session ID"""

        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id:
            return None
        session_dictionary = SessionAuth.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            user_id = session_dictionary["user_id"]
            return user_id
        if "created_at" not in session_dictionary:
            return None

        created_at = session_dictionary["created_at"]
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        else:
            return session_dictionary["user_id"]
