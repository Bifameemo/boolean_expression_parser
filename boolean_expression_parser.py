from enum import Enum, auto
from typing import NamedTuple

class TokenType(Enum):
    BRA = auto()
    KET = auto()

    NOT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    IMPLIES = auto()

    VAR = auto()

OPS = {"NOT": TokenType.NOT,
       "AND": TokenType.AND,
       "OR": TokenType.OR,
       "XOR": TokenType.XOR,
       "IMPLIES": TokenType.IMPLIES}

class Token(NamedTuple):
    type: TokenType
    value: str

def is_part_of_op_or_var(char: str) -> bool:
    return not char.isspace() and char != "(" and char != ")"

# lexer
def tokenise(expr: str) -> list[Token]:
    expr = expr.upper()
    tokenised_expr: list[Token] = []

    i = 0
    while i < len(expr):
        match expr[i]:
            case "(":
                tokenised_expr.append(Token(TokenType.BRA, "("))
            case ")":
                tokenised_expr.append(Token(TokenType.KET, ")"))
            case s if is_part_of_op_or_var(s):
                # read entire word
                word = ""
                while i < len(expr) and is_part_of_op_or_var(expr[i]):
                    word += expr[i]
                    i += 1
                i -= 1

                if word in OPS:
                    tokenised_expr.append(Token(OPS[word], word))
                else:
                    tokenised_expr.append(Token(TokenType.VAR, word))
            case _:
                assert expr[i].isspace(), expr[i]
                pass
        i += 1

    return tokenised_expr

def main():
    expr = "(  P and Q implies R ) xOR (P    and\tnot R implies    not Q)"

    tokenised_expr = tokenise(expr)
    for token in tokenised_expr:
        print(token.type.name, token.value)

if __name__ == "__main__":
    main()
