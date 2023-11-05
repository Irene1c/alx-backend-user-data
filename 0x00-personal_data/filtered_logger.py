#!/usr/bin/env python3
""" Filtered logger """
import logging
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """ Function that returns the log message obfuscated """
    for i in fields:
        pattern = f'{i}=[^{separator}]+'
        message = re.sub(pattern, f'{i}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Method that filters values in incoming log records """

        log_message = record.getMessage()
        f_message = filter_datum(self.fields, RedactingFormatter.REDACTION,
                                 log_message, RedactingFormatter.SEPARATOR)
        record.msg = f_message
        return super().format(record)
