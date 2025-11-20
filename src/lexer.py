from ply import lex # importing the lex lexer module

reserved = {
    # logical operators
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT",

    # control flow
    "BREAK": "BREAK",
    "ELIF": "ELIF",
    "ELSE": "ELSE",
    "FOR": "FOR",
    "IF": "IF",
    "IN": "IN",
    "WHILE": "WHILE",
    #"CONTINUE": "CONTINUE",

    # functions / return
    "FUNC": "FUNCTION",
    "RETURN": "RETURN",

    # Threading
    "THREAD": "THREAD",
    "RUN": "RUN",
    #"JOIN": "JOIN",
    #"LOCK": "LOCK",
    #"UNLOCK": "UNLOCK",

    # networking / protocols
    "ARP": "ARP",
    "HTTP": "HTTP",
    "ICMP": "ICMP",
    "SOCKET": "SOCKET",
    "TCP": "TCP",
    "UDP": "UDP",
    # "WS": "WS",
}

tokens = [
    # literals and identifiers
    "NUMBER",
    "TEXT",
    "BOOL",
    "IDENTIFIER",
    "NEWLINE",
    "COMMENT",

    # assignment and punctuation
    "ASSIGN",
    "COMMA",

    # arithmetic operators
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",

    # comparison operators
    "EQ",
    "NEQ",
    "LT",
    "GT",
    "LEQ",
    "GEQ",

    # grouping
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
] + list(reserved.values())

t_ignore_COMMENT = r'\#.*'