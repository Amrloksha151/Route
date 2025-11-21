from sys import argv
from .parser import parser

def main():
    if len(argv) > 1:
        filename = argv[1]
        with open(filename, 'r') as file:
            data = file.read()
        result = parser.parse(data)
        print(result)
    else:
        print("Route Interactive Parser V1.0. Type your commands below. To exit, press Ctrl+D.")
        while True:
            try:
                s = input('route> ')
            except EOFError:
                break
            result = parser.parse(s)
            print(result)

if __name__ == "__main__":
    main()