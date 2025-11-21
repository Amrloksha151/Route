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
                 | 
                 | NEWLINE'''
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

# While loop
def p_while_statement(p):
    '''while_statement : WHILE expression LBRACE loop_statements RBRACE'''
    p[0] = ('while', p[2], p[4])

def p_loop_statements(p):
    '''loop_statements : statements 
                       | BREAK NEWLINE'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [('break',)]

# For loop
def p_for_statement(p):
    '''for_statement : FOR IDENTIFIER IN expression LBRACE loop_statements RBRACE''' # add continue later
    p[0] = ('for', p[2], p[4], p[6])

# Function definition
def p_function_definition(p):
    '''function_definition : FUNCTION IDENTIFIER LPAREN optional_parameters RPAREN LBRACE function_statements RBRACE'''
    p[0] = ('function', p[2], p[4], p[7])

def p_optional_parameters(p):
    '''optional_parameters : parameter_list
                           | empty'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA IDENTIFIER
                      | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_function_statements(p):
    '''function_statements : statements 
                           | RETURN expression NEWLINE'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [('return', p[2])]

# Expression rules
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LEQ expression
                  | expression GT expression
                  | expression GEQ expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression'''
    if p[1] == 'NOT':
        p[0] = ('unop', p[1], p[2])
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_expression_uminus_upplus(p):
    '''expression : MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS'''
    p[0] = ('unop', p[1], p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', float(p[1]) if '.' in p[1] else int(p[1]))

def p_expression_text(p):
    '''expression : TEXT'''
    p[0] = ('text', p[1][1:-1])  # Remove quotes