#!/usr/bin/env python3
""" Auth module """
from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Function that defines which routes don't need authentication
        Returns True if the path is not in the list of strings excluded_paths
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for ex_path in excluded_paths:
            if path == ex_path or path + '/' == ex_path:
                return False
            elif ex_path.endswith('*') and path.startswith(
                    ex_path.rstrip('*')):
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Request validation"""
        if request is None:
            return None

        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method"""
        return None
