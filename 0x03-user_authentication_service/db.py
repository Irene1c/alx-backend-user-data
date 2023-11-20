#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that saves the user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ returns the first row found in the users table"""

        user_1 = self._session.query(User).filter_by(**kwargs).first()
        if user_1 is None:
            raise NoResultFound()
        return user_1

    def update_user(self, user_id: int, **kwargs) -> None:
        """update the user’s attributes"""

        user = self.find_user_by(id=user_id)
        if user:
            attr = set(User.__dict__.keys())
            for key in kwargs:
                if key not in attr:
                    raise ValueError()

            for key, val in kwargs.items():
                setattr(user, key, val)
            self._session.commit()
