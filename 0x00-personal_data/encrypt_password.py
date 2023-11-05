#!/usr/bin/env python3
""" Encrypting passwords with bcrypt """
import bcrypt


def hash_password(password: str) -> bytes:
    """function that expects a password argument and
        returns a salted, hashed password
    """

    psswd = password.encode('utf-8')  # encode to bytes
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(psswd, salt)

    return hashed_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function that validates that the provided password
        matches the hashed password
    """

    passwd = password.encode('utf-8')
    if bcrypt.checkpw(passwd, hashed_password):
        return True
    else:
        return False
