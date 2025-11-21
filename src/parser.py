from ply import yacc # importing the yacc parser module
from .lexer import tokens

# Define precedence and associativity of operators
precedence = (
    # Evalualted Last
    ('right', 'ASSIGN'),

    ('left', 'OR'),
    ('left', 'AND'),

    ('nonassoc', 'EQ', 'NEQ', 'LT', 'LEQ', 'GT', 'GEQ'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),

    ('right', 'NOT'),
    ('right', 'UMINUS', 'UPLUS'),
    # Evaluated First
)