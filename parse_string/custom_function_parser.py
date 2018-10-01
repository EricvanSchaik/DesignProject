from antlr4 import *
from gen.FunctionLexer import FunctionLexer
from gen.FunctionParser import FunctionParser
from parse_string.basic_function_visitor import BasicFunctionVisitor
from parse_string.error_listener import FunctionErrorListener
from parse_string.parse_exception import ParseException
import pandas as pd


class CustomFunctionParser:

    def __init__(self, expr: str, names: list):
        self.expr = expr

        # Determine variables used from names
        self.variables = []
        for name in names:
            if name in self.expr:
                self.variables.append(name)

        # Parse expression
        self.parsed_expr = self.parse()

    def parse(self):
        """
        Parses the expression string and turns it into a python readable string (with variables).
        Passes a parse exception when the expression string is invalid.
        :return: Readable python string with variables.
        """
        # Build parser from string
        parser = FunctionParser(CommonTokenStream(FunctionLexer(InputStream(self.expr))))

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
        except ParseException:
            # Pass parse exception
            raise

    def evaluate_row(self, row: dict):
        """
        Replaces the variable names with their values taken from the row dictionary and evaluates
        the resulting python expression.
        :param row: Dictionary containing variable (column) names with their respective value
        :return: The result of the expression evaluated using eval()
        """
        # Make a copy of the parsed expression string
        copy = self.parsed_expr

        # Check for every variable whether it's in the expression
        for var in self.variables:
            if var in copy:
                # Replaces variable name with its value in parentheses (for negative numbers)
                copy = copy.replace(var, "(" + str(row[var]) + ")")
        return eval(copy)

    def evaluate_single(self, x):
        """
        Replaces the variable name with its value and evaluates the resulting python expression.
        :param x: value of variable in parsed expression
        :return: The result of the expression evaluated using eval()
        """
        if pd.notna(x):
            return eval(self.parsed_expr.replace(self.variables[0], "(" + str(x) + ")"))
