// Generated from C:/Users/Eric/PycharmProjects/DesignProject/parse_string\Function.g4 by ANTLR 4.7
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link FunctionParser}.
 */
public interface FunctionListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterVarExpr(FunctionParser.VarExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitVarExpr(FunctionParser.VarExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code sqrtExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterSqrtExpr(FunctionParser.SqrtExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code sqrtExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitSqrtExpr(FunctionParser.SqrtExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code bracketExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterBracketExpr(FunctionParser.BracketExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code bracketExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitBracketExpr(FunctionParser.BracketExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code powExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPowExpr(FunctionParser.PowExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code powExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPowExpr(FunctionParser.PowExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMultExpr(FunctionParser.MultExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMultExpr(FunctionParser.MultExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumExpr(FunctionParser.NumExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumExpr(FunctionParser.NumExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code plusExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPlusExpr(FunctionParser.PlusExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code plusExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPlusExpr(FunctionParser.PlusExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link FunctionParser#multOp}.
	 * @param ctx the parse tree
	 */
	void enterMultOp(FunctionParser.MultOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link FunctionParser#multOp}.
	 * @param ctx the parse tree
	 */
	void exitMultOp(FunctionParser.MultOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link FunctionParser#plusOp}.
	 * @param ctx the parse tree
	 */
	void enterPlusOp(FunctionParser.PlusOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link FunctionParser#plusOp}.
	 * @param ctx the parse tree
	 */
	void exitPlusOp(FunctionParser.PlusOpContext ctx);
}