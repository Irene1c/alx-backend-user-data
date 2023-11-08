#!/usr/bin/env python3
""" Basic auth module """
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ base64 encoding """

        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None

        en_string = authorization_header.split(' ')
        return en_string[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Function that returns the decoded value of a Base64 string"""

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            d_str = base64.b64decode(
                    base64_authorization_header, validate=True)
            return d_str.decode('utf-8')
        except (binascii.Error, TypeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Function that returns the user email and password
            from the Base64 decoded value
        """

        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_psswd = decoded_base64_authorization_header.split(':')
        return tuple(user_psswd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Function that returns the User instance based
            on his email and password
        """
        from models.user import User

        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        v_psswd = user.is_valid_password(user_pwd)
        if not v_psswd:
            return None

        return user
