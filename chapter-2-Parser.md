# ⇁ Parsing
we transformed the raw source code into a series of tokens.
The **parser** we’ll write in this chapter takes those tokens and transforms them again to an even richer
Before we can produce that representation, we need to define it. That’s the
subject of this chapter.

### ⇁ how do evaluate an arithmetic expression like this
`1 + 2 * 3 - 4`
you know that the multiplication is evaluated before
the addition or subtraction. One way to visualize that precedence is using a tree.

![tree](https://raw.githubusercontent.com/rzksobhy27/lox/main/imgs/tree-evaluate.png)

# ⇁ Context-Free Grammars

takes a set of atomic pieces it calls its “alphabet”. Then it defines a set of “strings” that are “in” the grammar. Each string is a sequence of “letters” in the alphabet.

we are now on a different level

where alphabet consists of characters and each characters is an entire **token**
and a “string” is a sequence of tokens—an entire expression.

so basically
- **alphabet** is the source code we give
- **string** is the our output we take


