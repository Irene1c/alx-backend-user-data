#!/usr/bin/env python3
""" Encrypting passwords with bcrypt """
import bcrypt


def hash_password(password: str) -> bytes:
    """function that expects a password argument and
        returns a salted, hashed password
    """

    password = password.encode('utf-8')  # encode to bytes
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(password, salt)

    return hashed_passwd
