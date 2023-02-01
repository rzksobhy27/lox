# ⇁ Scanning

The first step in any compiler or interpreter is scanning
The scanner takes source code list of characters and transforms it into a higher level format as a list of **tokens**

# ⇁ how it works

it is not that hard pretty much a switch statement

# ⇁ Structures 

### ⇁ **Tokens** enum

`Tokens` enum lists all of our possible tokens including

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

### ⇁ `Token` class

```python
from typing import Union
from dataclasses import dataclass

@dataclass
class Token:
    token: Tokens
    line: int
    literal: Union[str, float, None]
```

### ⇁ the `Scanner` class

```python
class Scanner:
    def __init__(self, source: list[str]):
        self.source = source
        self.idx = 0
        self.line = 1

    def createToken(self, token, literal=None):
        return Token(token, self.line, literal)

    def isAtEnd(self):
        return self.idx >= len(self.source)

    # increments `self.idx` and returns current character
    def next(self):
        if self.isAtEnd():
            return "\0"

        current = self.idx
        self.idx += 1
        return self.source[current]

    # returns current character but doesn't increment `self.idx`
    def peek(self):
        if self.isAtEnd():
            return "\0"

        return self.source[self.idx]

    # our `scan` method
    def scan(self):
        while not self.isAtEnd():
            assert False, "not implemented"
```

> we don't always scan on character at a time some times our token is more than one like `==` or a string literal like `"foo"` this is why we can't just iterate over `source` instead we keep track of current `idx` ourselves

> For error reporing we also keep track of current line in source file

# ⇁ The `Scan` method
The scan method is not scary at all it just checks if `token` matches one of the tokens in `Token`

### ⇁ 1 character tokens
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
            elif token == " " or token == "\t" or token == "\r":
                # ignore some characters
                pass
            elif token == "\n":
                self.line += 1
            elif token == "\0":
                break
            else:
                print("[ERROR] unexpected token `{}` at line {}".format(token, self.line))
```

### ⇁ 1-2 character tokens 

for this we will need one more method to add how ever to do this we will need one more method the `match()` method which will check if the next character is what we expect to be
- if it is then it consumes that character and returns `True`
- if it isn't then it just returns `False`

``` python
    def match(self, expected):
        if self.peek() != expected:
            return False

        # consume the character
        self.next()
        return True
```

now we can scan 1-2 char tokens

```python
            elif token == "/":
                yield self.createToken(Tokens.SLASH)
            elif token == "=":
                yield self.createToken(Tokens.EQUAL_EQUAL if self.match("=") else Tokens.EQUAL)
            elif token == "!":
                yield self.createToken(Tokens.BANG_EQUAL if self.match("=") else Tokens.BANG)
            elif token == ">":
                yield self.createToken(Tokens.GREATER_EQUAL if self.match("=") else Tokens.GREATER)
            elif token == "<":
                yield self.createToken(Tokens.LESS_EQUAL if self.match("=") else Tokens.LESS)
            elif token == " " or token == "\t" or token == "\r":
```

### ⇁ string literals

strings are usually the characters between the staring and enclosing `"` mark

```python
            elif token == '"':
                string = self.string()
                yield self.createToken(Tokens.STRING, string)
```

to keep our code clean we will use the `string()` method which will consume all characters between the staring and enclosing `"` mark and return the string

```python
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
```

### ⇁ number literals

all numbers in our languages are floats at runtime

```python
            elif token = '"':
                string = self.string()
                yield self.createToken(Tokens.STRING, string)
            elif token.isdigit():
                number = self.number()
                yield self.createToken(Tokens.NUMBER, number)
```

and our `number()` method

```python
        string = self.source[start:end]
        string = "".join(string)

        return string


    def number(self):
        # get the number consumed on the main loop
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
```

### ⇁ identifiers and keywords

identifiers and keywords need some special treatment because a word might be a builtin **keyword** or just a normal **identifier**

the way we will do it is very simple
- first we will scan the whole word
- then we will match the result with our list of keywords
- if it exists we will return a keyword token
- else we will return an identifier literal

```python
                yield self.createToken(Tokens.STRING, string)
            elif token.isdigit():
                number = self.number()
                yield self.createToken(Tokens.NUMBER, number)
            elif token.isalpha():
                yield self.identifier()
            else:
                print("[ERROR] unexpected token `{}` at line {}".format(token, self.line))
```

and our `identifier()` method

```python
        number = float(number)

        return number

    def identifier(self):
        start = self.idx - 1

        while self.peek().isalpha() or self.peek().isdigit():
            self.next()

        end = self.idx

        identifier = self.source[start:end]
        identifier = "".join(identifier)
```

and like that we scanned the **word**<br />

to check if the **word** is a keywords we will create a python dictionary of key, value pairs where **key** is the keyword literal and **value** is the keyword value in our `Tokens` Enum

```python
keywords = {
    "or": Tokens.OR,
    "and": Tokens.AND,
    "if": Tokens.IF,
    "else": Tokens.ELSE,
    "var": Tokens.VAR,
    "function": Tokens.FUNCTION,
    "nil": Tokens.NIL,
    "true": Tokens.TRUE,
    "false": Tokens.FALSE
}
```

and now going to out `identifier()` method

```python
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
```

# ⇁ Testing the scanner

now our scanner is complete lets test it out

we will create an file say **example.lox**

```
({})
+ - * /
= ==
! !=
> >=
< <=
"foo" 123.5
or and
bar
```

- The first thing we will need to do is to read source file That is not hard to do in python

```python
path = "./example.lox"
file = open(path, "r")

# Reading source file
source = file.read()

file.close()
```

- and now we Scan it

```python
# we need list source characters
# because our scanner takes list[str]
scanner = Scanner(list(source))

# and we print it
for token in scanner.scan():
    print("Token: {}, literal: {}, line: {}".format(token.token, token.literal, token.line))
```

the result should be something like
```txt
Token: Tokens.LEFT_PAREN, literal: None, line: 1
Token: Tokens.LEFT_BRACE, literal: None, line: 1
Token: Tokens.RIGHT_BRACE, literal: None, line: 1
Token: Tokens.RIGHT_PAREN, literal: None, line: 1
Token: Tokens.PLUS, literal: None, line: 2
Token: Tokens.MINUS, literal: None, line: 2
Token: Tokens.STAR, literal: None, line: 2
Token: Tokens.SLASH, literal: None, line: 2
Token: Tokens.EQUAL, literal: None, line: 3
Token: Tokens.EQUAL_EQUAL, literal: None, line: 3
Token: Tokens.BANG, literal: None, line: 4
Token: Tokens.BANG_EQUAL, literal: None, line: 4
Token: Tokens.GREATER, literal: None, line: 5
Token: Tokens.GREATER_EQUAL, literal: None, line: 5
Token: Tokens.LESS, literal: None, line: 6
Token: Tokens.LESS_EQUAL, literal: None, line: 6
Token: Tokens.STRING, literal: foo, line: 7
Token: Tokens.NUMBER, literal: 123.5, line: 7
Token: Tokens.OR, literal: None, line: 8
Token: Tokens.AND, literal: None, line: 8
Token: Tokens.IDENTIFIER, literal: bar, line: 9
```

and that is pretty much it now we can
- Scan tokens like `>`, `!=`, `+`
- Strings like `"foo"`
- numbers like `123.4`
- identifiers
- and finally keywords like `or`, `else`
