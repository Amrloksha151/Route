from sys import argv
from parser import parser

def main():
    if len(argv) > 1:
        filename = argv[1]
        with open(filename, 'r') as file:
            data = file.read()
        AST = parser.parse(data)
        print(AST)
        #run(AST)
    else:
        print("Route Interactive Interpreter V1.0. By Amr Loksha and Omar Faisal \nType your commands below. To exit, press Ctrl+C.")
        while True:
            try:
                s = input('route> ')
            except KeyboardInterrupt:
                print("\nExiting Route Interactive Interpreter. Goodbye!")
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
        try: 
            return self.vars.get(name, None)
        except KeyError:
            print(f"{name} is not defined.")

class Functions:
    def __init__(self):
        self.funcs = {}

    def set(self, name, statements, variables):
        self.funcs[name] = (statements, variables)

    def get(self, name):
        try: 
            return self.funcs.get(name, None)
        except KeyError:
            print(f"Function {name} is not defined.")

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
    # Additional node evaluations would go here

def run(program):
    variables = Variables()
    functions = Functions()
    for statement in program[1]:
        evaluate_node(statement, variables, functions)

if __name__ == "__main__":
    main()