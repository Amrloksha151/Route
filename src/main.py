from sys import argv, exit
from parser import parser
import socket, threading
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    if len(argv) > 1:
        filename = argv[1]
        if not filename.endswith('.route'):
            print(f"{Fore.RED}Error: File must have a .route extension.{Style.RESET_ALL}")
            exit(1)
        with open(filename, 'r') as file:
            data = file.read()
        AST = parser.parse(data)
        #print(AST)
        run(AST)
    else:
        print(f"{Fore.CYAN}Route Interactive Interpreter V1.0. By Amr Loksha and Omar Faisal \nType your commands below. To exit, press Ctrl+C.{Style.RESET_ALL}")
        while True:
            try:
                s = input('route> ')
            except KeyboardInterrupt:
                print(f"{Fore.GREEN}\nExiting Route Interactive Interpreter. Goodbye!{Style.RESET_ALL}")
                break
            AST = parser.parse(s)
            #print(AST)
            run(AST)

# Interpreter Functionality would go here to process the AST

# Variables storage
class Variables:
    def __init__(self):
        self.vars = {}

    def set(self, name, value):
        self.vars[name] = value

    def delete(self, name):
        if name in self.vars:
            del self.vars[name]

    def get(self, name):
        if name not in self.vars:
            print(f"{Fore.RED}Error: Variable {name} is not defined.{Style.RESET_ALL}")
            exit(1)
        return self.vars.get(name, None)

class Functions:
    def __init__(self):
        self.funcs = {}

    def set(self, name, statements, paramaters):
        self.funcs[name] = (statements, paramaters)

    def get(self, name):
        if name not in self.funcs:
            print(f"{Fore.RED}Error: Function {name} is not defined.{Style.RESET_ALL}")
            exit(1)
        return self.funcs.get(name, None)

# Evaluator and other components would be implemented here

def evaluate_node(node, variables, functions=None):
    node_type = node[0]

    if node_type == 'input':
        return input(node[1] if node[1] else '')
    elif node_type == 'output':
        print(evaluate_node(node[1], variables, functions))
    elif node_type == 'text':
        return node[1]
    elif node_type == 'number':
        return node[1]
    elif node_type == 'bool':
        return node[1]
    elif node_type == 'assign':
        variables.set(node[1], evaluate_node(node[2], variables, functions))
    elif node_type == 'identifier':
        return variables.get(node[1])
    elif node_type == 'int_conv':
        return int(evaluate_node(node[1], variables, functions))
    elif node_type == 'float_conv':
        return float(evaluate_node(node[1], variables, functions))
    elif node_type == 'binop':
        left = evaluate_node(node[2], variables, functions)
        right = evaluate_node(node[3], variables, functions)
        op = node[1]
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
    elif node_type == 'unop':
        operand = evaluate_node(node[2], variables, functions)
        op = node[1]
        if op == '-':
            return -operand
        elif op == 'not':
            return not operand
        elif op == '+':
            return +operand
    elif node_type == 'if':
        condition = evaluate_node(node[1], variables, functions)
        if condition:
            for stmt in node[2]:
                evaluate_node(stmt, variables, functions)
        else:
            if len(node) > 3 and isinstance(node[3], list):
                for elif_clause in node[3]:
                    elif_condition = evaluate_node(elif_clause[1], variables, functions)
                    if elif_condition:
                        for stmt in elif_clause[2]:
                            evaluate_node(stmt, variables, functions)
                        return
                if len(node) > 4 and node[4]:
                    for stmt in node[4][1]:
                        evaluate_node(stmt, variables, functions)
            elif len(node) > 3 and node[3]:
                for stmt in node[3][1]:
                    evaluate_node(stmt, variables, functions)
    elif node_type == 'while':
        condition = evaluate_node(node[1], variables, functions)
        while condition:
            for stmt in node[2]:
                evaluate_node(stmt, variables, functions)
            condition = evaluate_node(node[1], variables, functions)
    elif node_type == 'for':
        var_name = node[1]
        expression = evaluate_node(node[2], variables, functions)
        if not isinstance(expression, int):
            print(f"{Fore.RED}Error: For loop expression must evaluate to an integer.{Style.RESET_ALL}")
            exit(1)
        for i in range(expression): # add lists later
            variables.set(var_name, i)
            for stmt in node[4]:
                evaluate_node(stmt, variables, functions)
    elif node_type == 'function':
        func_name = node[1]
        parameters = node[2]
        statements = node[3]
        functions.set(func_name, statements, parameters)
    elif node_type == 'func_call':
        func_name = node[1]
        args = node[2]
        func = functions.get(func_name)
        local_vars = Variables()
        if args:
            for i in range(args):
                try:
                    local_vars.set(func[1][i], evaluate_node(args[i], variables, functions))
                except IndexError:
                    print(f"{Fore.RED}Error: Incorrect number of arguments for function '{func_name}'.{Style.RESET_ALL}")
                    exit(1)
        for statement in func[0]:
            evaluate_node(statement, local_vars, functions)
    elif node_type == 'break':
        raise StopIteration
    elif node_type == 'socket':
        s = {
            'protocol': node[1],
            'host': evaluate_node(node[2], variables, functions),
            'port': evaluate_node(node[3], variables, functions),
            'socket': None
        }
        if s['protocol'].lower() == 'tcp':
            s['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif s['protocol'].lower() == 'udp':
            s['socket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print(f"{Fore.RED}Error: Unsupported protocol '{s['protocol']}'.{Style.RESET_ALL}")
            exit(1)
        if not isinstance(s['port'], int):
            print(f"{Fore.RED}Error: Port must be an integer.{Style.RESET_ALL}")
            exit(1)
        elif s['port'] < 0 or s['port'] > 65535:
            print(f"{Fore.RED}Error: Port must be between 0 and 65535.{Style.RESET_ALL}")
            exit(1)
        
        if not isinstance(s['host'], str):
            print(f"{Fore.RED}Error: Host must be a string.{Style.RESET_ALL}")
            exit(1)
        return s
    elif node_type == 'connect':
        socket = variables.get(node[1])
        try:
            socket['socket'].connect((socket['host'], socket['port']))
        except Exception as e:
            print(f"{Fore.RED}Error: Could not connect to {socket['host']}:{socket['port']} - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'send':
        socket = variables.get(node[1])
        data = node[2].encode()
        try:
            socket['socket'].sendall(data) # Works for both TCP and UDP
        except Exception as e:
            print(f"{Fore.RED}Error: Could not send data - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'receive':
        socket = variables.get(node[1])
        num_bytes = node[2]
        if isinstance(num_bytes, float):
            print(f"{Fore.RED}Error: Number of bytes to receive must be an integer.{Style.RESET_ALL}")
            exit(1)
        try:
            data = socket['socket'].recv(num_bytes)
            return data.decode()
        except Exception as e:
            print(f"{Fore.RED}Error: Could not receive data - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'close':
        socket = variables.get(node[1])
        try:
            socket['socket'].close()
        except Exception as e:
            print(f"{Fore.RED}Error: Could not close socket - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'bind':
        socket = variables.get(node[1])
        try:
            socket['socket'].bind((socket['host'], socket['port']))
        except Exception as e:
            print(f"{Fore.RED}Error: Could not bind to {socket['host']}:{socket['port']} - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'listen':
        socket = variables.get(node[1])
        try:
            socket['socket'].listen(node[2])
        except Exception as e:
            print(f"{Fore.RED}Error: Could not listen on socket - {e}{Style.RESET_ALL}")
            exit(1)
    elif node_type == 'thread':
        func_name = node[1]
        args = node[2]
        def thread_function():
            local_vars = Variables()
            func = functions.get(func_name)
            if args:
                for i in range(len(args)):
                    try:
                        local_vars.set(func[1][i], evaluate_node(args[i], variables, functions))
                    except IndexError:
                        print(f"{Fore.RED}Error: Incorrect number of arguments for function '{func_name}' in thread.{Style.RESET_ALL}")
                        exit(1)
            for statement in func[0]:
                evaluate_node(statement, local_vars, functions)
        return threading.Thread(target=thread_function)
    elif node_type == 'run_thread':
        thread = variables.get(node[1])
        if not isinstance(thread, threading.Thread):
            print(f"{Fore.RED}Error: Variable '{node[1]}' is not a thread.{Style.RESET_ALL}")
            exit(1)
        thread.start()
    else:
        print(f"{Fore.RED}Error: Unknown node type '{node_type}'.{Style.RESET_ALL}")
        exit(1)
    # Additional node evaluations would go here

def run(program):
    variables = Variables()
    functions = Functions()
    try:
        program[1]
    except TypeError:
        pass
    else:
        for statement in program[1]:
            evaluate_node(statement, variables, functions)


if __name__ == "__main__":
    main()