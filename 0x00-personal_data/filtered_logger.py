#!/usr/bin/env python3
""" Obfuscating through Regex-ing """
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
