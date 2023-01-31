# Scanning

The first step in any compiler or interpreter is scanning
The scanner takes source code list of characters and transforms it into a higher level format as a list of **tokens**

# ⇁ how it works

it is not that hard pretty much a switch statement

# ⇁ the code

- The first thing we will need to do is to read source file That is not hard to do in python

```python
path = "./example.lox"
file = open(path, "r")

# Reading source file
source = file.read()

file.close()
```

### ⇁ Structures 

- We will need our `Tokens` enum which lists all of our possible tokens

```python
from enum import Enum, auto

class Tokens(Enum):
    # 1 char tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

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
```

> These are our tokens for now we may add more tokens in the future

- and of course our `Token` class
```python
from typing import Union
from dataclasses import dataclass

@dataclass
class Token:
    token: Tokens
    line: int
    literal: Union[str, float, None]
```

- and our `Scanner` class which will scan our code

```python
class Scanner:
    def __init__(self, source: list[str]):
        self.source = source
        self.idx = 0
        self.line = 1

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scan(self):
        while not self.isAtEnd():
            pass
```

> we don't always scan on character at a time some times our token is more than one like `==` or a string literal like `"foo"` this is why we can't just iterate over `source` and we need to keep track of current index ourselves

> For error reporing we also keep track of current line in source file


### ⇁ Our tools
These are the `Scanner` method we will pretty much need

- The `next()` function increments `self.idx` and give us the current character

```python
    def isAtEnd(self):
        return self.current >= len(self.source)

    def next(self):
        current = self.idx
        self.idx += 1
        return self.source[current]

    def scan(self):
```

- We will also need the `peek()` function which give us the current character with out incrementing `self.idx`

```python
    def next(self):
        current = self.idx
        self.idx += 1
        return self.source[current]

    def peek(self):
        if self.isAtEnd():
            return "\0"

        return self.source[self.idx]

    def scan(self):
```

- every time we will need return a `Token` we will need to create an instance of it this gets annoying specially with tha fact that only **Literals** will take a value for the `Literal` field this is why we will create the `createToken` method which will automatically use `self.line` as a value for the `line` field and also has a default value for `Literal`

```python
    def createToken(self, token, literal = None):
        return Token(token, self.line, literal)

    def next(self):
        current = self.idx
```

and that is it this all we will need to implement our `Scanner`

### ⇁ The `Scan` method
The scan method is not scary at all it will just check if `token` matches one of our `Tokens`

- First we will 1 character tokens
```python
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
            else:
                print("[ERROR] unexpected token `{}` at line {}".format(token, self.line))
```

> you can create a list before the loop and keep appending the **Tokens** as you go I used `yield` because I just like it that is not for any technical reason


