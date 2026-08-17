from enum import Enum, auto
from typing import NamedTuple


class TokenType(Enum):
    BRA = auto()
    KET = auto()
    OP = auto()
    VAR = auto()


class OpType(Enum):
    NIL = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    IMPLIES = auto()


# allowed aliases for all operations
OP_ALIASES = {
    "NOT": OpType.NOT,
    "AND": OpType.AND,
    "&&": OpType.AND,
    "OR": OpType.OR,
    "||": OpType.OR,
    "XOR": OpType.XOR,
    "IMPLIES": OpType.IMPLIES,
}

OP_PRECEDENCES = {
    OpType.NIL: -1,
    OpType.NOT: 3,
    OpType.AND: 2,
    OpType.OR: 2,
    OpType.XOR: 2,
    OpType.IMPLIES: 1,
}


# C-style tagged union (but with a struct)
class Token(NamedTuple):
    type: TokenType

    # TokenType.OP
    op: OpType = OpType.NIL
    precedence: int = OP_PRECEDENCES[op]

    # TokenType.VAR
    name: str = ""


# lexer
def tokenise(expr: str) -> list[Token]:
    def is_part_of_op_or_var(char: str) -> bool:
        return not char.isspace() and char != "(" and char != ")"

    expr = expr.upper()
    tokenised_expr: list[Token] = []

    i = 0
    while i < len(expr):
        match expr[i]:
            case "(":
                tokenised_expr.append(Token(TokenType.BRA))
            case ")":
                tokenised_expr.append(Token(TokenType.KET))
            case s if is_part_of_op_or_var(s):
                # read entire word
                word = ""
                while i < len(expr) and is_part_of_op_or_var(expr[i]):
                    word += expr[i]
                    i += 1
                i -= 1

                if word in OP_ALIASES:
                    tokenised_expr.append(
                        Token(
                            TokenType.OP,
                            OP_ALIASES[word],
                        )
                    )
                else:
                    tokenised_expr.append(Token(TokenType.VAR, name=word))
            case _:
                assert expr[i].isspace(), expr[i]
                pass
        i += 1

    return tokenised_expr


# see https://en.wikipedia.org/wiki/Shunting_yard_algorithm for algorithm details
def infix_to_postfix(tokens: list[Token]) -> list[Token]:
    operator_stack: list[Token] = []
    postfix: list[Token] = []

    for token in tokens:
        match token.type:
            case TokenType.VAR:
                postfix.append(token)
            case TokenType.OP:
                while (
                    len(operator_stack) > 0
                    and operator_stack[-1].type == TokenType.OP
                    and operator_stack[-1].precedence >= token.precedence
                ):
                    postfix.append(operator_stack.pop())
                operator_stack.append(token)
            case TokenType.BRA:
                operator_stack.append(token)
            case TokenType.KET:
                while (
                    len(operator_stack) > 0 and operator_stack[-1].type != TokenType.BRA
                ):
                    postfix.append(operator_stack.pop())

                assert len(operator_stack) > 0, "Mismatched parentheses."
                operator_stack.pop()

    while len(operator_stack) > 0:
        assert operator_stack[-1].type != TokenType.BRA, "Mismatched parentheses."
        postfix.append(operator_stack.pop())

    return postfix


def main():
    expr = (
        "(  P and Q implies R ) xOR (P    &&\tnot R implies    not Q) ||  (P or not P)"
    )

    tokenised_expr = tokenise(expr)
    for token in tokenised_expr:
        print(
            token.type.name, token.name, token.op.name if token.op != OpType.NIL else ""
        )

    postfix_tokens = infix_to_postfix(tokenised_expr)
    print(postfix_tokens)


if __name__ == "__main__":
    main()
