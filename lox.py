#! /usr/bin/env pypy

from enum import Enum, auto
import sys
from dataclasses import dataclass
from typing import Union


class Tokens(Enum):
    # 1 char tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto()
    STAR = auto()

    # 1-2 char tokens
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

@dataclass
class Token:
    token: Tokens
    line: int
    literal: Union[str, float, None]


class Scanner:
    pass


if __name__ == "__main__":
    argv = sys.argv

    if len(argv) == 1:
        print("USAGE: %s <FILE>" % argv[0])
        print("[ERROR] no <FILE> is provided")
        sys.exit(1)

    source_path = argv[1]
    source_file = open(source_path, "r")

    source = source_file.read()
    source = list(source)

    source_file.close()
