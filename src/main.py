from sys import argv, exit
from parser import parser
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    if len(argv) > 1:
        filename = argv[1]
        with open(filename, 'r') as file:
            data = file.read()
        AST = parser.parse(data)
        print(AST)
        #run(AST)
    else:
        print(f"{Fore.CYAN}Route Interactive Interpreter V1.0. By Amr Loksha and Omar Faisal \nType your commands below. To exit, press Ctrl+C.{Style.RESET_ALL}")
        while True:
            try:
                s = input('route> ')
            except KeyboardInterrupt:
                print(f"{Fore.GREEN}\nExiting Route Interactive Interpreter. Goodbye!{Style.RESET_ALL}")
                break
            AST = parser.parse(s)
            print(AST)
            #run(AST)

# Interpreter Functionality would go here to process the AST

# Variables storage
class Variables:
    def __init__(self):
        self.vars = {}

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            print(f"{Fore.RED}Error: Variable {name} is not defined.{Style.RESET_ALL}")
            exit(1)
        return self.vars.get(name, None)

class Functions:
    def __init__(self):
        self.funcs = {}

    def set(self, name, statements, variables):
        self.funcs[name] = (statements, variables)

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
        pass
    elif node_type == 'for':
        pass
    
    # Additional node evaluations would go here

def run(program):
    variables = Variables()
    functions = Functions()
    for statement in program[1]:
        evaluate_node(statement, variables, functions)

if __name__ == "__main__":
    main()