# Angelica Munyao
# Homework 7:
# CLite program parser.

# We will need the lexer module to get a CLite program's tokens.
import lexer

# We will need to import the ast module to make use of the classes defined in it. The class objects are required in
# building the abstract syntax representation of a given CLite program.
import ast

# We will need the sys library to run the program in the terminal.
import sys



# Define a class for a CLite syntax error exception that inherits from the "Exception" class.
class CLiteSyntaxError(Exception):
    # CLiteSyntaxError constructor.
    def __init__(self, illTok, expectedTok, *customMsg):
        self.illTok = illTok[2] # Get the illegal token.
        self.lineNum = illTok[3] # Get the line number of the illegal token.
        self.expectedTok = expectedTok # Get the expected token.
        self.customMsg = (customMsg[0] if len(customMsg) > 0 else '') # Get a custom message if available.

    # CLiteSyntaxError object string representation.
    def __str__(self):
        if self.customMsg != '':
            # Return the error message with the illegal token, the error and the line number.
            return "Syntax Error: Unexpected " + self.illTok + " on line number " + str(self.lineNum) + ". " + \
                   self.customMsg + "."
        else:
            # Return the error message with the illegal token, the expected token and the line number.
            return "Syntax Error: Unexpected " + self.illTok + " on line number " + str(self.lineNum) + ". Expected: " \
                   + self.expectedTok + "."



# Define a class for a CLite program parsing object.
class Parser:
    # Parser constructor.
    # Given the file name of a CLite program, it retrieves the tokens from it for parsing.
    def __init__(self, filename):
        # Create a lexer object.
        lex = lexer.Lexer()

        # Create a token generator from the Lexer object.
        self.tokens = lex.token_generator(filename)

        # Initialize the current token.
        # This is the first token of the program.
        self.currToken = next(self.tokens)

        # Create a Program object into which we add declarations and statements.
        self.parseTree = ast.Program()

    # Parse the CLite program.
    def parse(self):
        # Return the final abstract syntax tree representation of the CLite program.
        return self.program()



    def program(self):
        """
        Program         ⇒  int  main ( ) { Declarations Statements }
        """
        # Check for 'int'.
        if self.currToken[0] == lexer.Lexer.KWDINT:
            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for 'main'.
            if self.currToken[2] == 'main':
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Check for '('.
                if self.currToken[0] == lexer.Lexer.PARENLEFT:
                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for ')'.
                    if self.currToken[0] == lexer.Lexer.PARENRIGHT:
                        # Move to the next token.
                        self.currToken = next(self.tokens)

                        # Check for '{'.
                        if self.currToken[0] == lexer.Lexer.CURLYLEFT:
                            # Move to the next token.
                            self.currToken = next(self.tokens)

                            # Check for type keyword.
                            if self.currToken[0] in (lexer.Lexer.KWDBOOL, lexer.Lexer.KWDINT, lexer.Lexer.KWDFLOAT):
                                # Check for declarations and add them to the Program object.
                                self.declarations()

                            # Unexpected token encountered.
                            else:
                                raise CLiteSyntaxError(self.currToken, 'Type Keyword i.e. int, float, bool')

                            # Check for statement start tokens.
                            if self.currToken[0] in (lexer.Lexer.SEMICOLON, lexer.Lexer.CURLYLEFT, lexer.Lexer.ID,
                                                        lexer.Lexer.KWDIF, lexer.Lexer.KWDWHILE, lexer.Lexer.KWDPRINT):
                                # Check for statements and add them to the Program object.
                                self.statements()

                            # Unexpected token encountered.
                            else:
                                raise CLiteSyntaxError(self.currToken, 'Statement i.e. assignment, if, while, print, '
                                                                       'statement block or semicolon')

                            # Check for '}'.
                            if self.currToken[0] == lexer.Lexer.CURLYRIGHT:
                                # The program has been successfully parsed.
                                return self.parseTree

                            # Unexpected token encountered.
                            else:
                                raise CLiteSyntaxError(self.currToken, '}')

                        # Unexpected token encountered.
                        else:
                            raise CLiteSyntaxError(self.currToken, '{')

                    # Unexpected token encountered.
                    else:
                        raise CLiteSyntaxError(self.currToken, ')')

                # Unexpected token encountered.
                else:
                    raise CLiteSyntaxError(self.currToken, '(')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, 'main')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'int')



    def declarations(self):
        """
        Declarations    ⇒  { Declaration }
        Declaration     ⇒  Type  Identifier  ;
        Type            ⇒  int | bool | float
        """
        # Look for declarations to store in the Program object. The first token in a declaration is
        # a variable keyword.
        while self.currToken[0] in (lexer.Lexer.KWDBOOL, lexer.Lexer.KWDINT, lexer.Lexer.KWDFLOAT):
            # Capture the token representation to create a Declaration object.
            type = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for an identifier.
            if self.currToken[0] == lexer.Lexer.ID:
                # Capture the Id value to create a Declaration object.
                identify = self.currToken[2]

                # Check whether the variable has already been defined.
                # The variable has already been defined; raise an exception.
                if identify in self.parseTree.declarations.keys():
                    raise CLiteSyntaxError(self.currToken, 'N/A', 'The variable has been previously declared')

                # Variable has not been defined yet.
                else:
                    # Create a Declaration object.
                    declare = ast.Declaration(type, identify)

                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for ';'.
                    if self.currToken[0] == lexer.Lexer.SEMICOLON:
                        # Move to the next token.
                        self.currToken = next(self.tokens)

                        # Add the declaration to the Program object.
                        self.parseTree.addDecl(declare)

                    # Unexpected token encountered.
                    else:
                        raise CLiteSyntaxError(self.currToken, 'a semicolon')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, 'Identifier')



    def statements(self):
        """
        Statements      ⇒  { Statement }
        """
        # Look for statements to store in the Program object. The first token in a statement can be ';', '{',
        # an identifier, 'if', 'while' or 'print'.
        while self.currToken[0] in (lexer.Lexer.SEMICOLON, lexer.Lexer.CURLYLEFT, lexer.Lexer.ID,
                                    lexer.Lexer.KWDIF, lexer.Lexer.KWDWHILE, lexer.Lexer.KWDPRINT):
            # Create a Statement object (either a SemiStatement, BlockStatement, Assignment, IfWhileStatement or
            # PrintStatement object).
            aStatement = self.statement()

            # A statement was successfully created. Add it to the Program object.
            self.parseTree.addStmnt(aStatement)



    def statement(self):
        """
        Statement       ⇒  ; | Block | Assignment | IfStatement | WhileStatement | PrintStatement
        """
        # Create a semicolon, block, assignment, if, while or print statement depending on the encountered token.
        if self.currToken[0] == lexer.Lexer.SEMICOLON:
            return self.semi()

        elif self.currToken[0] == lexer.Lexer.CURLYLEFT:
            return self.block()

        elif self.currToken[0] == lexer.Lexer.ID:
            return self.assignment()

        elif self.currToken[0] == lexer.Lexer.KWDIF:
            return self.ifstatement()

        elif self.currToken[0] == lexer.Lexer.KWDWHILE:
            return self.whilestatement()

        elif self.currToken[0] == lexer.Lexer.KWDPRINT:
            return self.printstatement()

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'Statement i.e. assignment, if, while, print, statement block or semicolon')



    def semi(self):
        """
        ;
        """
        # Create a SemiStatement object.
        semiState = ast.SemiStatement()

        # Move to the next token.
        self.currToken = next(self.tokens)

        # Return the SemiStatement object.
        return semiState



    def block(self):
        """
        Block           ⇒  { Statements }
        """
        # Check for '{'.
        if self.currToken[0] == lexer.Lexer.CURLYLEFT:
            # Move to the next token.
            self.currToken = next(self.tokens)

            # Look for statements to store in the BlockStatement object. The first token in a statement can be ';', '{',
            # an identifier, 'if', 'while' or 'print'.
            # Create a list to store the found statements.
            stateList = []

            while self.currToken[0] in (lexer.Lexer.SEMICOLON, lexer.Lexer.CURLYLEFT, lexer.Lexer.ID,
                                        lexer.Lexer.KWDIF, lexer.Lexer.KWDWHILE, lexer.Lexer.KWDPRINT):
                # Create a Statement object (either a SemiStatement, BlockStatement, Assignment, IfWhileStatement or
                # PrintStatement object).
                aStatement = self.statement()

                # A statement was successfully created. Add it to the list of statements.
                stateList.append(aStatement)

            # Check for '}'.
            if self.currToken[0] == lexer.Lexer.CURLYRIGHT:
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Create a BlockStatement object.
                aBlock = ast.BlockStatement(stateList)

                # Return the statement.
                return aBlock

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, '}')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, '{')



    def assignment(self):
        """
        Assignment      ⇒  Identifier = Expression ;
        """
        # Check for an identifier.
        if self.currToken[0] == lexer.Lexer.ID:
            # Check if the identifier has been declared.
            if self.currToken[2] in self.parseTree.declarations.keys():
                # Capture the identifier to create an Assignment object.
                identify = self.currToken[2]

                # Move to the next token.
                self.currToken = next(self.tokens)

                # Check for '='.
                if self.currToken[0] == lexer.Lexer.ASSIGN:
                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for an expression and capture it to create an Assignment object.
                    expr = self.expression()

                    # Check for ';'.
                    if self.currToken[0] == lexer.Lexer.SEMICOLON:
                        # Move to the next token.
                        self.currToken = next(self.tokens)

                        # Create an Assignemt object.
                        assign = ast.Assignment(identify, expr)

                        # Return the assignment object.
                        return assign

                    # Unexpected token encountered.
                    else:
                        raise CLiteSyntaxError(self.currToken, ';')

                # Unexpected token encountered.
                else:
                    raise CLiteSyntaxError(self.currToken, '=')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, 'N/A', 'Undeclared variable encountered')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'Identifier')



    def ifstatement(self):
        """
        IfStatement     ⇒  if ( Expression ) Statement [ else Statement ]
        """
        # Check for 'if'.
        if self.currToken[0] == lexer.Lexer.KWDIF:
            # Capture the keyword to create an IfWhileStatement object.
            kwd = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for '('.
            if self.currToken[0] == lexer.Lexer.PARENLEFT:
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Check for an expression and capture it to create an IfWhileStatement object.
                expr = self.expression()

                # Check for ')'.
                if self.currToken[0] == lexer.Lexer.PARENRIGHT:
                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for a statement and capture it to create an IfWhileStatement object.
                    aStatement = self.statement()

                    # Check for an optional 'else'.
                    if self.currToken[0] == lexer.Lexer.KWDELSE:
                        # Move to the next token.
                        self.currToken = next(self.tokens)

                        # Check for another statement and capture it to create an IfWhileStatement object.
                        elseStatement = self.statement()

                        # Create an IfWhileStatement with an 'else'.
                        ifState = ast.IfWhileStatement(kwd, expr, aStatement, elseStatement)

                    # Create an IfWhileStatement without an 'else'.
                    else:
                        ifState = ast.IfWhileStatement(kwd, expr, aStatement)

                    # Return the IfWhileStatement object.
                    return ifState

                # Unexpected token encountered.
                else:
                    raise CLiteSyntaxError(self.currToken, ')')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, '(')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'if')



    def whilestatement(self):
        """
        WhileStatement  ⇒  while ( Expression ) Statement
        """
        # Check for 'while'.
        if self.currToken[0] == lexer.Lexer.KWDWHILE:
            # Capture the keyword to create an IfWhileStatement object.
            kwd = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for '('.
            if self.currToken[0] == lexer.Lexer.PARENLEFT:
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Check for an expression and capture it to create an IfWhileStatement object.
                expr = self.expression()

                # Check for ')'.
                if self.currToken[0] == lexer.Lexer.PARENRIGHT:
                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for a statement and capture it to create an IfWhileStatement object.
                    aStatement = self.statement()

                    # Create the IfWhileStatement object.
                    whileState = ast.IfWhileStatement(kwd, expr, aStatement)

                    # Return the IfWhileStatement object.
                    return whileState

                # Unexpected token encountered.
                else:
                    raise CLiteSyntaxError(self.currToken, ')')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, '(')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'while')



    def printstatement(self):
        """
        PrintStatement  ⇒  print( Expression ) ;
        """
        # Check for 'print'.
        if self.currToken[0] == lexer.Lexer.KWDPRINT:
            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for '('.
            if self.currToken[0] == lexer.Lexer.PARENLEFT:
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Check for an expression and capture it to create an IfWhileStatement object.
                expr = self.expression()

                # Check for ')'.
                if self.currToken[0] == lexer.Lexer.PARENRIGHT:
                    # Move to the next token.
                    self.currToken = next(self.tokens)

                    # Check for ';'.
                    if self.currToken[0] == lexer.Lexer.SEMICOLON:
                        # Move to the next token.
                        self.currToken = next(self.tokens)

                        # Create the IfWhileStatement object.
                        printState = ast.PrintStatement(expr)

                        # Return the IfWhileStatement object.
                        return printState

                    # Unexpected token encountered.
                    else:
                        raise CLiteSyntaxError(self.currToken, ';')

                # Unexpected token encountered.
                else:
                    raise CLiteSyntaxError(self.currToken, ')')

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, '(')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'print')



    def expression(self):
        """
        Expression      ⇒  Conjunction { || Conjunction }
        """
        # Check for a conjunction expression and capture it to create a BinaryExpr object.
        left = self.conjunction()

        # Check for '||' until there are no more.
        while self.currToken[0] == lexer.Lexer.BOOLOR:
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another conjunction expression and capture it to create a BinaryExpr object.
            right = self.conjunction()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def conjunction(self):
        """
        Conjunction     ⇒  Equality { && Equality }
        """
        # Check for an equality expression and capture it to create a BinaryExpr object.
        left = self.equality()

        # Check for '&&' until there are no more.
        while self.currToken[0] == lexer.Lexer.BOOLAND:
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another equality expression and capture it to create a BinaryExpr object.
            right = self.equality()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def equality(self):
        """
        Equality        ⇒  Relation [ EquOp Relation ]
        """
        # Check for a relation expression and capture it to create a BinaryExpr object.
        left = self.relation()

        # Check for optional EqOp operators.
        if self.currToken[0] in (lexer.Lexer.EQ, lexer.Lexer.NOTEQ):
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another relation expression and capture it to create a BinaryExpr object.
            right = self.relation()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def relation(self):
        """
        Relation        ⇒  Addition [ RelOp Addition ]
        """
        # Check for an addition expression and capture it to create a BinaryExpr object.
        left = self.addition()

        # Check for optional RelOp operators.
        if self.currToken[0] in (lexer.Lexer.LESS, lexer.Lexer.LESSEQ, lexer.Lexer.GREAT, lexer.Lexer.GREATEQ):
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another addition expression and capture it to create a BinaryExpr object.
            right = self.addition()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def addition(self):
        """
        Addition        ⇒  Term { AddOp Term }
        """
        # Check for a term expression and capture it to create a BinaryExpr object.
        left = self.term()

        # Check for addOps operators.
        while self.currToken[0] in (lexer.Lexer.ADD, lexer.Lexer.SUBTRACT):
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another term expression and capture it to create a BinaryExpr object.
            right = self.term()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def term(self):
        """
        Term            ⇒  Exponent { MulOp Exponent }
        """
        # Check for an exponent expression and capture it to create a BinaryExpr object.
        left = self.exponent()

        # Check for mulOps operators.
        while self.currToken[0] in (lexer.Lexer.MULTIPLY, lexer.Lexer.DIVIDE, lexer.Lexer.REMAINDER):
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for another exponent expression and capture it to create a BinaryExpr object.
            right = self.exponent()

            # Create a BinaryExpr object.
            left = ast.BinaryExpr(operator, left, right)

        # Return the BinaryExpr object.
        return left



    def exponent(self):
        """
        Exponent        ⇒  {Factor **} Factor
        """
        # Check for a factor expression and capture it to create an exponent expression. There must be at least one factor.
        aFactor = self.factor()

        # Initialize a variable to be used while creating an exponent expression with more than one factor expression
        # and '**' operator.
        aBinaryExpr = ''

        # Check for '**' operators.
        if self.currToken[0] == lexer.Lexer.POWER:
            # Capture the operator to create a BinaryExpr object.
            operator = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Create a BinaryExpr object.
            aBinaryExpr = ast.BinaryExpr(operator, aFactor, self.exponent())

        # Check whether right was given an expression.
        if aBinaryExpr == '':
            # Return the expression.
            return aFactor

        else:
            # Return the BinaryExpr object.
            return aBinaryExpr



    def factor(self):
        """
        Factor          ⇒  [ UnaryOp ] Primary
        """
        # Check for optional UnaryOp operator.
        if self.currToken[0] in (lexer.Lexer.SUBTRACT, lexer.Lexer.NOT):
            # Capture the operator to create a UnaryExpr object.
            op = self.currToken[0]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for a factor expression and capture it to create a Unary object. There could be more than one '-'.
            expr = self.factor()

            # Return a UnaryExpr object.
            return ast.UnaryExpr(expr, op)

        # There is no UnaryOp.
        else:
            # Check for a primary expression and return it.
            return self.primary()



    def primary(self):
        """
        Primary         ⇒  Identifier | IntLit | FloatLit | ( Expression ) | true | false
        """
        # Check for an identifier.
        if self.currToken[0] == lexer.Lexer.ID:
            if self.currToken[2] in self.parseTree.declarations.keys():
                # Capture the identifier to create an IdExpr object.
                identify = self.currToken[2]

                # Move to the next token.
                self.currToken = next(self.tokens)

                # Create and return an IdExpr object.
                return ast.IdExpr(identify)

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, 'N/A', 'Undeclared variable encountered')


        # Check for a literal.
        elif self.currToken[0] in (lexer.Lexer.INTLIT, lexer.Lexer.FLOATLIT, lexer.Lexer.KWDTRUE, lexer.Lexer.KWDFALSE):
            # Capture the literal to create a LitExpr object.
            literal = self.currToken[2]

            # Move to the next token.
            self.currToken = next(self.tokens)

            # Create and return a LitExpr object.
            return ast.LitExpr(literal)


        # Check for '('.
        elif self.currToken[0] == lexer.Lexer.PARENLEFT:
            # Move to the next token.
            self.currToken = next(self.tokens)

            # Check for an expression and capture it.
            expr = self.expression()

            # Check for ')'.
            if self.currToken[0] == lexer.Lexer.PARENRIGHT:
                # Move to the next token.
                self.currToken = next(self.tokens)

                # Return the expression.
                return expr

            # Unexpected token encountered.
            else:
                raise CLiteSyntaxError(self.currToken, ')')

        # Unexpected token encountered.
        else:
            raise CLiteSyntaxError(self.currToken, 'Identifier, literal or expression')



if __name__ == '__main__':
    # Check whether a file name has been given.
    # Error: A file name was not given.
    if (len(sys.argv) < 2):
        exit("Error: No file name given. Please input a file name to open and process.")

    else:
        # Create a Parser object.
        parser = Parser(sys.argv[1])

        # Parse the given CLite program using the Parser object. Catch a CLite syntax error thrown.
        try:
            asr = parser.parse()
            print(asr)

            # Run the CLite program and print its result.
            print("\n")
            print("Result:") 
            asr.run()

        # A CLite syntax error was raised; print the error message from the caught exception.
        except CLiteSyntaxError as e:
            print(e)


