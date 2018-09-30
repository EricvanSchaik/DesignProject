from antlr4 import *
from gen.FunctionLexer import FunctionLexer
from gen.FunctionParser import FunctionParser
from parse_string.basic_function_visitor import BasicFunctionVisitor
from parse_string.error_listener import FunctionErrorListener
from parse_string.parse_exception import ParseException


def dict_test_data():
    return {'Time': 0.006042,
            'Ax': 4.922654,
            'Ay': -1.163624,
            'Az': -6.876393,
            'Gx': 60.302734,
            'Gy': -66.955566,
            'Gz': -51.208496,
            'Mx': -84.090243,
            'My': -41.312628,
            'Mz': -43.363610,
            'T': 25.560,
            'Vector': 8.536470}


def parse_string(string):
    # Build parser from string
    parser = FunctionParser(CommonTokenStream(FunctionLexer(InputStream(string))))

    # Add custom error listener to parser
    parser._listeners = [FunctionErrorListener()]
    parser.buildParseTrees = True
    try:
        # Create parse tree
        tree = parser.expr()

        # Visit parse tree with custom visitor
        visitor = BasicFunctionVisitor()
        visitor.visit(tree)

        # Print statement for debugging purposes
        # print(visitor.debug)

        # Return result string from visitor
        return visitor.string
    except ParseException as e:
        # Catch parse exception and handle it
        return e.args


def evaluate_parsed_string(row, string):
    # Copy string
    copy = string

    # Check for every variable in row whether it's in the string
    for var in row.keys():
        if var in string:
            # Replace variable name with its value in parentheses (for negative numbers)
            copy = copy.replace(var, "(" + str(row[var]) + ")")
    return eval(copy)


parse_result = parse_string("sqrt(Ax^2 + Ay^2 + Az^2)")
print(evaluate_parsed_string(dict_test_data(), parse_result))
