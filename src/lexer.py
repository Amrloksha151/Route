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
    "CONNECT": "CONNECT",
    "SEND": "SEND",
    "RECEIVE": "RECEIVE",
    "CLOSE": "CLOSE",
    "BIND": "BIND",
    "LISTEN": "LISTEN",

    # other keywords
    "OUTPUT": "OUTPUT",
    "INPUT": "INPUT",
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
t_NEWLINE = r'\n+'
t_TEXT = r'\"([^\\\n]|(\\.))*?\"'
t_BOOL = r'\b(true|false)\b'
t_NUMBER = r'\b\d+(\.\d+)?\b'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_error(t): # further modification later
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# reserved words mapping
# functions / return
t_FUNCTION = r'FUNC'
t_RETURN = r'RETURN'

# control flow
t_IF = r'IF'
t_ELSE = r'ELSE'
t_ELIF = r'ELIF'
t_FOR = r'FOR'
t_IN = r'IN'
# t_CONTINUE = r'CONTINUE'
t_WHILE = r'WHILE'
t_BREAK = r'BREAK'

# logical operators
t_AND = r'AND'
t_OR = r'OR'
t_NOT = r'NOT'

# threading
t_THREAD = r'THREAD'
t_RUN = r'RUN'
# t_JOIN = r'JOIN'
# t_LOCK = r'LOCK'
# t_UNLOCK = r'UNLOCK'

# networking / protocols
t_ARP = r'ARP'
t_HTTP = r'HTTP'
t_ICMP = r'ICMP'
# t_WS = r'WS'
t_SOCKET = r'SOCKET'
t_TCP = r'TCP'
t_UDP = r'UDP'
t_CONNECT = r'CONNECT'
t_SEND = r'SEND'
t_RECEIVE = r'RECEIVE'
t_CLOSE = r'CLOSE'
t_BIND = r'BIND'
t_LISTEN = r'LISTEN'
t_OUTPUT = r'OUTPUT'
t_INPUT = r'INPUT'

lexer = lex.lex()