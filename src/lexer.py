from ply import lex # importing the lex lexer module

reserved = {
    "true": "TRUE",
    "false": "FALSE",
    "INT": "INTEGER",
    "FLOAT": "FLOAT",

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
    "ARGS": "ARGS",
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
    "CONNECT": "CONNECT",
    "SEND": "SEND",
    "RECEIVE": "RECEIVE",
    "CLOSE": "CLOSE",
    "BIND": "BIND",
    "LISTEN": "LISTEN",
    "PORT": "PORT",

    # other keywords
    "OUTPUT": "OUTPUT",
    "INPUT": "INPUT",
}

tokens = [
    # literals and identifiers
    "NUMBER",
    "TEXT",
    "IDENTIFIER",
    "SEMICOLON",

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

t_ASSIGN = r'='
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ignore_NEWLINE = r'\r\n|\r|\n'
t_TEXT = r'(\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\')'
t_NUMBER = r'\b\d+(\.\d+)?\b'
t_ignore = ' \t'
t_SEMICOLON = r';'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_error(t): # further modification later
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex(lextab=None, debug=False)