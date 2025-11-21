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

def p_program(p):
    '''program : statements'''
    p[0] = ('program', p[1])

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement(p):
    '''statement : expression NEWLINE
                 | assignment NEWLINE
                 | output_statement NEWLINE
                 | input_statement NEWLINE
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_definition
                 | return_statement NEWLINE'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_output_statement(p):
    '''output_statement : OUTPUT expression'''
    p[0] = ('output', p[2])

def p_input_statement(p):
    '''input_statement : IDENTIFIER ASSIGN INPUT optional_prompt'''
    if p[4]:
        p[0] = ('input', p[1], p[4])
    else:
        p[0] = ('input', p[1])

def p_optional_prompt(p):
    '''optional_prompt : TEXT
                       | empty'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    p[0] = None

# If statement with optional elif and else
def p_if_statement(p):
    '''if_statement : IF expression LBRACE statements RBRACE optional_elif optional_else'''
    if p[7]:
        p[0] = ('if', p[2], p[4], p[6], p[7]) if p[6] else ('if', p[2], p[4], p[7])
    elif p[6]:
        p[0] = ('if', p[2], p[4], p[6])
    else:
        p[0] = ('if', p[2], p[4])

def p_optional_elif(p):
    '''optional_elif : ELIF expression LBRACE statements RBRACE optional_elif
                     | empty'''
    if len(p) > 2:
        if p[6]:
            p[0] = [('elif', p[2], p[4])] + p[6]
        else:
            p[0] = [('elif', p[2], p[4])]
    else:
        p[0] = None

def p_optional_else(p):
    '''optional_else : ELSE LBRACE statements RBRACE
                     | empty'''
    if len(p) > 2:
        p[0] = ('else', p[3])
    else:
        p[0] = None