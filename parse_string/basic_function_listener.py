from gen.FunctionListener import FunctionListener
from gen.FunctionParser import FunctionParser


class BasicFunctionListener(FunctionListener):

    def __init__(self):
        # self.row = row
        self.variables = []
        self.string = ""

    def enterExpr(self, ctx: FunctionParser.ExprContext):
        if ctx.NUMBER():
            # a constant
            self.string += ctx.getText()
            if "." or "," in ctx.getText():
                value = float(ctx.getText())
            else:
                value = int(ctx.getText())
        elif ctx.VAR():
            # a variable
            self.string += ctx.getText()
            self.variables.append(ctx.getText())
        elif ctx.sqrt():
            # square root of an expression
            self.string += "("
            pass
        elif ctx.LBRACKET():
            # an expression between brackets
            self.string += "("
            pass
        else:
            # two expressions with an operation
            self.string += " op "
            pass

    def exitExpr(self, ctx: FunctionParser.ExprContext):
        if ctx.sqrt():
            # square root
            self.string += ")**2"
            pass
        elif ctx.RBRACKET():
            # expression between brackets
            self.string += ")"
            pass
        elif ctx.OP():
            # two expressions with an operation
            self.string += "op"
            pass
