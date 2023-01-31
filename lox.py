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

    # Keywords
    OR = auto()
    AND = auto()
    IF = auto()
    ELSE = auto()
    VAR = auto()
    FUNCTION = auto()
    NIL = auto()
    TRUE = auto()
    FALSE = auto()


keywords = {
    "or": Tokens.OR,
    "and": Tokens.AND,
    "if": Tokens.IF,
    "else": Tokens.ELSE,
    "var": Tokens.VAR,
    "function": Tokens.FUNCTION,
    "nil": Tokens.NIL,
    "true": Tokens.TRUE,
    "false": Tokens.FALSE,
}


@dataclass
class Token:
    token: Tokens
    line: int
    literal: Union[str, float, None]


class Scanner:
    def __init__(self, source: list[str]):
        self.source = source
        self.idx = 0
        self.line = 1

    def isAtEnd(self):
        return self.idx >= len(self.source)

    def next(self):
        current = self.idx
        self.idx += 1
        if self.isAtEnd():
            return "\0"

        return self.source[current]

    def peek(self):
        if self.isAtEnd():
            return "\0"

        return self.source[self.idx]

    def match(self, expected):
        if self.peek() != expected:
            return False

        # consume the character
        self.next()
        return True

    def string(self):
        start = self.idx

        while self.next() != '"':
            if self.peek() == "\n":
                print("[ERROR] unterminated string at line %i" % self.line)
                sys.exit(1)

        end = self.idx - 1

        string = self.source[start:end]
        string = "".join(string)

        return string

    def number(self):
        start = self.idx - 1

        while self.peek().isdigit():
            self.next()

        if self.peek() == ".":
            # consume the `.`
            self.next()

            while self.peek().isdigit():
                self.next()

        end = self.idx

        number = self.source[start:end]
        number = "".join(number)
        number = float(number)

        return number

    def identifier(self):
        start = self.idx - 1

        while self.peek().isalpha() or self.peek().isdigit():
            self.next()

        end = self.idx

        identifier = self.source[start:end]
        identifier = "".join(identifier)

        keyword = keywords.get(identifier)
        if keyword != None:
            return self.createToken(keyword)
        else:
            return self.createToken(Tokens.IDENTIFIER, identifier)

    def createToken(self, token, literal=None):
        return Token(token, self.line, literal)

    def scan(self):
        while not self.isAtEnd():
            # Get the token
            token = self.next()

            if token == "(":
                yield self.createToken(Tokens.LEFT_PAREN)
            elif token == ")":
                yield self.createToken(Tokens.RIGHT_PAREN)
            elif token == "{":
                yield self.createToken(Tokens.LEFT_BRACE)
            elif token == "}":
                yield self.createToken(Tokens.RIGHT_BRACE)
            elif token == ",":
                yield self.createToken(Tokens.COMMA)
            elif token == ".":
                yield self.createToken(Tokens.DOT)
            elif token == "+":
                yield self.createToken(Tokens.PLUS)
            elif token == "-":
                yield self.createToken(Tokens.MINUS)
            elif token == "*":
                yield self.createToken(Tokens.STAR)
            elif token == "/":
                yield self.createToken(Tokens.SLASH)
            elif token == "=":
                yield self.createToken(
                    Tokens.EQUAL_EQUAL if self.match("=") else Tokens.EQUAL
                )
            elif token == "!":
                yield self.createToken(
                    Tokens.BANG_EQUAL if self.match("=") else Tokens.BANG
                )
            elif token == ">":
                yield self.createToken(
                    Tokens.GREATER_EQUAL if self.match("=") else Tokens.GREATER
                )
            elif token == "<":
                yield self.createToken(
                    Tokens.LESS_EQUAL if self.match("=") else Tokens.LESS
                )
            elif token == '"':
                string = self.string()
                yield self.createToken(Tokens.STRING, string)
            elif token.isdigit():
                number = self.number()
                yield self.createToken(Tokens.NUMBER, number)
            elif token.isalpha():
                yield self.identifier()
            elif token == " " or token == "\t" or token == "\r":
                # ignore some characters
                pass
            elif token == "\n":
                self.line += 1
            elif token == "\0":
                break
            else:
                print(
                    "[ERROR] unexpected token `{}` at line {}".format(token, self.line)
                )

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

    scanner = Scanner(source)
    for token in scanner.scan():
        print(
            "Token: {}, literal: {}, line: {}".format(
                token.token, token.literal, token.line
            )
        )
