from antlr4 import *
from gen.FunctionLexer import FunctionLexer
from gen.FunctionParser import FunctionParser
from parse_string.basic_function_listener import BasicFunctionListener


def test1(string):
    tokens = CommonTokenStream(FunctionLexer(InputStream(string)))
    parser = FunctionParser(tokens)
    parser.buildParseTrees = True
    tree = parser.expr()
    listener = BasicFunctionListener()
    ParseTreeWalker.DEFAULT.walk(listener, tree)
    print(listener.string)
    pass


test1("1 + 2")
