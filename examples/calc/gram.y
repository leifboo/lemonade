
%left PLUS MINUS.
%left DIVIDE TIMES.

program ::= expr(A).   { print(A); }

expr(A) ::= expr(B) MINUS  expr(C).  { A = B - C; }
expr(A) ::= expr(B) PLUS   expr(C).  { A = B + C; }
expr(A) ::= expr(B) TIMES  expr(C).  { A = B * C; }
expr(A) ::= expr(B) DIVIDE expr(C).  { A = B / C; }
        
expr(A) ::= NUM(B). { A = B; }
