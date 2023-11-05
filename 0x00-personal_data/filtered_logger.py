#!/usr/bin/env python3
""" Filtered logger """
import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that returns a connector to the database"""

    h = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    u_name = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    psswd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db = os.environ.get('PERSONAL_DATA_DB_NAME')

    connect_obj = mysql.connector.connect(
            host=h, user=u_name, password=psswd, database=db)
    return connect_obj


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """ Function that returns the log message obfuscated """
    for i in fields:
        pattern = f'{i}=[^{separator}]+'
        message = re.sub(pattern, f'{i}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """ function that creates and configures a logger
        The logger should not propagate messages to other loggers
    """

    logger = logging.getLogger('user_data')
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = PII_FIELDS):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Method that filters values in incoming log records """

        log_message = record.getMessage()
        f_message = filter_datum(self.fields, RedactingFormatter.REDACTION,
                                 log_message, RedactingFormatter.SEPARATOR)
        record.msg = f_message
        return super().format(record)


def main() -> None:
    """ Function that obtains a database connection and retrieves all rows
        in the users table and displays each row under a filtered format
    """

    db = get_db()
    cursor = db.cursor(dictionary=True)  # dictionary cursor
    cursor.execute("SELECT * FROM users; ")
    result = cursor.fetchall()  # list of dictionaries
    cursor.close()
    db.close()

    logger = get_logger()

    for user in result:
        # Redact PII fields
        redact_info = {
            field: RedactingFormatter.REDACTION if field in PII_FIELDS
            else user.get(field)
            for field in PII_FIELDS + ("ip", "last_login", "user_agent")
        }

        # Format and log user info
        user_info = " ".join(
                f"{field}={val};" for field, val in redact_info.items())
        logger.info(user_info)


if __name__ == '__main__':
    main()
