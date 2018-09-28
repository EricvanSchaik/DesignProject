from gen.FunctionParser import FunctionParser
from gen.FunctionVisitor import FunctionVisitor


class BasicFunctionVisitor(FunctionVisitor):

    def __init(self):
        self.string = ""

    def visitExpr(self, ctx: FunctionParser.ExprContext):
        if ctx.NUMBER():
            self.string += ctx.getText()
        elif ctx.VAR():
            self.string += ctx.getText()
        elif ctx.sqrt():
            self.string += "("
            self.visitSqrt(ctx.sqrt())
            self.string += ")**2"
        elif ctx.LBRACKET():
            self.string += "("
            self.visitExpr(ctx.expr())
            self.string += ")"
        # TODO: finish this
        return self.visitChildren(ctx)

    def visitSqrt(self, ctx: FunctionParser.SqrtContext):
        return self.visitChildren(ctx)
