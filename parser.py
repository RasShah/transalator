class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.symbol_table = {}

    def error(self, msg):
        raise RuntimeError(f'Syntax error at token {self.current_token}: {msg}')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            self.error(f'Expected {token_type}')

    # Program ::= DeclarationList
    def parse_program(self):
        while self.current_token.type in ("INT", "BOOL"):
            self.parse_declaration()

        if self.current_token.type != "EOF":
            self.error("Unexpected token after end of program")

    # Declaration ::= Type VarList SEMICOLON
    def parse_declaration(self):
        var_type = self.parse_type()
        self.parse_var_list(var_type)
        self.eat("SEMICOLON")

    # Type ::= INT | BOOL
    def parse_type(self):
        if self.current_token.type == "INT":
            self.eat("INT")
            return "int"

        elif self.current_token.type == "BOOL":
            self.eat("BOOL")
            return "bool"

        else:
            self.error("Type expected")

    # VarList ::= VarInit VarListTail
    def parse_var_list(self, var_type):
        self.parse_var_init(var_type)

        while self.current_token.type == "COMMA":
            self.eat("COMMA")
            self.parse_var_init(var_type)

    # VarInit ::= ID | ID ASSIGN Expression
    def parse_var_init(self, var_type):
        if self.current_token.type != "ID":
            self.error("Identifier expected")

        var_name = self.current_token.value
        self.eat("ID")

        value = None

        if self.current_token.type == "ASSIGN":
            self.eat("ASSIGN")
            value = self.parse_expression(var_type)

        if var_name in self.symbol_table:
            self.error(f'Variable "{var_name}" already declared')

        self.symbol_table[var_name] = {
            "type": var_type,
            "value": value
        }

        print(f'Declared {var_name} of type {var_type} with value {value}')

    # Expression ::= IntExpr | BoolExpr
    def parse_expression(self, expected_type):
        if expected_type == "int":
            return self.parse_int_expr()

        elif expected_type == "bool":
            return self.parse_bool_expr()

        else:
            self.error("Unknown type for expression")

    # BoolExpr ::= TRUE | FALSE
    def parse_bool_expr(self):
        if self.current_token.type == "TRUE":
            self.eat("TRUE")
            return True

        elif self.current_token.type == "FALSE":
            self.eat("FALSE")
            return False

        else:
            self.error("Boolean expression expected")

    # IntExpr ::= Term IntExprTail
    def parse_int_expr(self):
        result = self.parse_term()

        while self.current_token.type in ("PLUS", "MINUS"):
            if self.current_token.type == "PLUS":
                self.eat("PLUS")
                result += self.parse_term()

            elif self.current_token.type == "MINUS":
                self.eat("MINUS")
                result -= self.parse_term()

        return result

    # Term ::= Factor TermTail
    def parse_term(self):
        result = self.parse_factor()

        while self.current_token.type in ("STAR", "SLASH"):
            if self.current_token.type == "STAR":
                self.eat("STAR")
                result *= self.parse_factor()

            elif self.current_token.type == "SLASH":
                self.eat("SLASH")
                denom = self.parse_factor()

                if denom == 0:
                    self.error("Division by zero")

                result //= denom

        return result

    # Factor ::= NUMBER | LPAREN IntExpr RPAREN
    def parse_factor(self):
        if self.current_token.type == "NUMBER":
            val = int(self.current_token.value)
            self.eat("NUMBER")
            return val

        elif self.current_token.type == "LPAREN":
            self.eat("LPAREN")
            val = self.parse_int_expr()
            self.eat("RPAREN")
            return val

        else:
            self.error("Factor expected")