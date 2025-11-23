from ply import yacc # importing the yacc parser module
from lexer import tokens

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
    '''statement : expression SEMICOLON
                 | assignment SEMICOLON
                 | output_statement SEMICOLON
                 | input_statement SEMICOLON
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_definition
                 | socket_statement SEMICOLON
                 | bind_statement SEMICOLON
                 | connect_statement SEMICOLON
                 | close_statement SEMICOLON
                 | listen_statement SEMICOLON
                 | send_statement SEMICOLON
                 | receive_statement SEMICOLON
                 | thread_statement SEMICOLON
                 | run_thread_statement SEMICOLON'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression
                  | IDENTIFIER ASSIGN assignment_statement'''
    p[0] = ('assign', p[1], p[3])

def p_assignment_statement(p):
    '''assignment_statement : input_statement
                            | socket_statement
                            | thread_statement
                            | integer_statement
                            | float_statement'''
    p[0] = p[1]

def p_integer_statement(p):
    '''integer_statement : INTEGER expression'''
    p[0] = ('int_conv', p[2])

def p_float_statement(p):
    '''float_statement : FLOAT expression'''
    p[0] = ('float_conv', p[2])

def p_output_statement(p):
    '''output_statement : OUTPUT expression'''
    p[0] = ('output', p[2])

def p_input_statement(p):
    '''input_statement : INPUT optional_prompt'''
    p[0] = ('input', p[2])

def p_optional_prompt(p):
    '''optional_prompt : TEXT
                       | empty'''
    p[0] = p[1][1:-1] if p[1] else None

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
    '''loop_statements : loop_statements loop_statement
                       | loop_statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_loop_statement(p):
    '''loop_statement : statement
                      | BREAK SEMICOLON'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('break',)

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
                           | RETURN expression SEMICOLON'''
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
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ('unop', p[1], p[2])

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

def p_expression_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('bool', True if p[1] == 'true' else False)

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = ('identifier', p[1])

def p_expression_function_call(p):
    '''expression : IDENTIFIER LPAREN optional_arguments RPAREN'''
    p[0] = ('func_call', p[1], p[3])

def p_optional_arguments(p):
    '''optional_arguments : argument_list
                          | empty'''
    p[0] = p[1]

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Socket operations
def p_socket_statement(p):
    '''socket_statement : SOCKET protocol TEXT PORT NUMBER'''
    p[0] = ('socket', p[2], p[3][1:-1], int(p[5]))

def p_protocol(p):
    '''protocol : TCP
                | UDP
                | HTTP
                | ARP
                | ICMP'''
    p[0] = p[1]

def p_bind_statement(p):
    '''bind_statement : BIND IDENTIFIER protocol TEXT PORT NUMBER
                      | BIND IDENTIFIER'''
    if len(p) == 7:
        p[0] = ('bind', p[2], p[3], p[4][1:-1], int(p[6]))
    else:
        p[0] = ('bind', p[2])

def p_connect_statement(p):
    '''connect_statement : CONNECT IDENTIFIER'''
    p[0] = ('connect', p[2])

def p_close_statement(p):
    '''close_statement : CLOSE IDENTIFIER'''
    p[0] = ('close', p[2])

def p_listen_statement(p):
    '''listen_statement : LISTEN IDENTIFIER NUMBER'''
    p[0] = ('listen', p[2], int(p[3]))

def p_send_statement(p):
    '''send_statement : SEND IDENTIFIER TEXT''' # change the text to an expression
    p[0] = ('send', p[2], p[3][1:-1])

def p_receive_statement(p):
    '''receive_statement : RECEIVE IDENTIFIER NUMBER'''
    p[0] = ('receive', p[2], int(p[3]))

def p_thread_statement(p):
    '''thread_statement : THREAD IDENTIFIER ARGS LPAREN optional_arguments RPAREN'''
    p[0] = ('thread', p[2], p[5])

def p_run_thread_statement(p):
    '''run_thread_statement : RUN IDENTIFIER'''
    p[0] = ('run_thread', p[2])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc(debug=False)