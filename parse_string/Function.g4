grammar Function;

// Parser rules
expr    : LBRACKET expr RBRACKET | expr OP expr
        | sqrt | NUMBER | VAR;
sqrt    : SQRT LBRACKET expr RBRACKET;

// Lexer rules
fragment DIGIT  : [0-9];
NUMBER          : DIGIT+ ([.,] DIGIT+)?;
SQRT            : 'sqrt';
VAR             : ([A-Z]|[a-z])+;
OP              : '+' | '-' | '*' | '/' | '^';
LBRACKET        : '(';
RBRACKET        : ')';
WHITESPACE      : ' ' -> skip;