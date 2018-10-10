// Generated from C:/Users/Eric/PycharmProjects/DesignProject/parse_string\Function.g4 by ANTLR 4.7
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link FunctionParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface FunctionVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarExpr(FunctionParser.VarExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code sqrtExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSqrtExpr(FunctionParser.SqrtExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code bracketExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBracketExpr(FunctionParser.BracketExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code powExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPowExpr(FunctionParser.PowExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code multExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultExpr(FunctionParser.MultExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumExpr(FunctionParser.NumExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code plusExpr}
	 * labeled alternative in {@link FunctionParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPlusExpr(FunctionParser.PlusExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link FunctionParser#multOp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultOp(FunctionParser.MultOpContext ctx);
	/**
	 * Visit a parse tree produced by {@link FunctionParser#plusOp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPlusOp(FunctionParser.PlusOpContext ctx);
}