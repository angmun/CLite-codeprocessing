# Angelica Munyao
# Homework 7:
# Generate the abstract syntax representation of CLite program.

# Get the token representations from the lexer module.
import lexer

# We will need the regular expression library to make use of regular expressions in our code.
import re

# A class that defines a Program object.
# Program is a singleton class; only one instance of this class is required for every Parser object created.
# As such, the data required from its object could be class data instead of instance data.
class Program:
    # Class variables: a dictionary of Declaration objects and a list of Statement objects.
    declarations = dict()
    statements = []


    # We do not require several instances of the Program class to initialize their own variables with various values;
    # only the class variables require modification.
    def __init__(self):
        pass


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "Program({0}, {1})".format(repr(Program.declarations), repr(Program.statements))


    # The string representation of the object.
    def __str__(self):
        # Create two long strings to represent the declarations and statements.
        decls = ""
        stmnts = ""

        # Since a dictionary is not ordered, the order in which declarations are printed may not be the order in which
        # they were written in the original CLite code.
        for decl in Program.declarations.values():
            decls += "\t" + str(decl[0]) + "\n"

        for stmnt in Program.statements:
            # Consider whether a statement has one or more newline characters in its string representation to determine
            # the appropriate indentation.
            stmnts += "\t" + str(stmnt).replace("\n", "\n\t") + "\n"

        # Return the appropriately formatted string representation of a Program object.
        return "int main()\n{\n" + decls + "\n" + stmnts + "}"


    # Add a Declaration object to the Program object's dictionary of Declaration objects.
    def addDecl(self, aDeclaration):
        # At this point, an identifier has yet to be initialized, so it has no value.
        Program.declarations[aDeclaration.id] = (aDeclaration, None)


    # Add a statement to the Program object's list of statements.
    # Statements can be a SemiStatement, Block, IfStatement, WhileStatement, PrintStatement or Assignment object.
    def addStmnt(self, aStatement):
        Program.statements.append(aStatement)


    # Evaluate the program.
    def run(self):
        for stmnt in Program.statements:
            stmnt.run()



# A class that defines a Declaration object.
class Declaration:
    # Initialize a dictionary of type keywords.
    typeDict = {lexer.Lexer.KWDINT:'int', lexer.Lexer.KWDFLOAT:'float', lexer.Lexer.KWDBOOL:'bool'}

    # Capture the type and identifier values of a declaration in a Declaration object.
    def __init__(self, type, identify):
        self.type = type
        self.id = identify


    # Make Declaration objects comparable; in particular, we are looking to see whether two Declaration objects have
    # the same identifier value.
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "Declaration({0},{1})".format(self.type, self.id)


    # The string representation of the object.
    def __str__(self):
        return "{0} {1};".format(Declaration.typeDict[self.type], self.id)



# A class that defines a SemiStatement object.
class SemiStatement:
    # The SemiStatement object has no variables to initialize.
    def __init__(self):
        pass


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "SemiStatement()"


    # The string representation of the object.
    def __str__(self):
        return ";"


    # The SemiStatement object has no data to manipulate for evaluation.
    def run(self):
        return



# a class that defines a BlockStatement object.
class BlockStatement:
    # The BlockStatement object takes a list of statements.
    def __init__(self, stmnts: list):
        self.stmnts = stmnts


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "BlockStatement({0})".format(repr(self.stmnts))


    # The string representation of the object.
    def __str__(self):
        # Create a long string to represent the statements.
        statements = ""

        for state in self.stmnts:
            # Consider whether a statement has one or more newline characters in its string representation to determine
            # the appropriate indentation.
            statements += "\t" + str(state).replace("\n", "\n\t") + "\n"

        #  Return the appropriately formatted representation of a BlockStatement object.
        return "{\n" + statements + "}"


    # Evaluate the BlockStatement object.
    def run(self):
        for stmnt in self.stmnts:
            stmnt.run()



# A class that defines an Assignment object.
class Assignment:
    # Capture the identifier and expression values of an assignment statement in an Assignment object.
    def __init__(self, identify, expr):
        self.id = identify
        self.expr = expr


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "Assignment({0},{1})".format(self.id, repr(self.expr))


    # The string representation of the object.
    def __str__(self):
        return "{0} = {1};".format(self.id, str(self.expr))


    # Evaluate the Assignment object.
    def run(self):
        # Evaluate the object's expression.
        value = self.expr.run()

        # Update the declarations dictionary with the value that the identifier represents.
        Program.declarations[self.id] = (Program.declarations[self.id][0], value)



# A class that defines an IfWhileStatement object.
class IfWhileStatement:
    # Initialize a dictionary of keywords.
    stateKwd = {lexer.Lexer.KWDIF:'if', lexer.Lexer.KWDWHILE:'while'}

    # Capture the statement type, expression and statement(s) values of an if/while statement in an IfStatement object.
    def __init__(self, kwd, expr, *stmnt):
        self.kwd = kwd
        self.expr = expr
        self.stmnt = stmnt[0]
        self.elsestmnt = (stmnt[1] if len(stmnt) > 1 else "")


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "IfWhileStatement({0},{1},{2},{3})".format(self.kwd, repr(self.expr), repr(self.stmnt), repr(self.elsestmnt))


    # The string representation of the object.
    def __str__(self):
        # Consider whether a statement is a block statement.
        if (str(self.stmnt).startswith("{")):
            statement = "\n" + str(self.stmnt)

        else:
            statement = "\n\t" + str(self.stmnt).replace("\n", "\n\t")

        # Consider whether an else's statement is empty or a block statement.
        if self.elsestmnt == "":
            elsestatement = ""

        elif (str(self.elsestmnt).startswith("{")):
            elsestatement = "\n\nelse\n" + str(self.stmnt)

        else:
            elsestatement = "\n\nelse\n\t" + str(self.elsestmnt).replace("\n", "\n\t")

        # Return the appropriately formatted string representation of an IfWhileStatement object.
        return "{0} ({1}) {2} {3}".format(IfWhileStatement.stateKwd[self.kwd], str(self.expr), statement, elsestatement)


    # Evaluate the IfWhileStatement object.
    def run(self):
        # Determine the value of the expression.
        boolVal = self.expr.run()

        # Evaluation of an if statement.
        if self.kwd == lexer.Lexer.KWDIF:
            # Check the value of the expression.
            if boolVal == 'true':
                # Evaluate the statement.
                self.stmnt.run()

            else:
                if self.elsestmnt != "":
                    # Evaluate the else statement.
                    self.elsestmnt.run()

                else:
                    return

        # Evaluation of a while statement.
        else:
            # Check the value of the expression and continue checking it after every iteration.
            while boolVal == "true":
                # Evaluate the statement.
                self.stmnt.run()

                # Update the value of the condition expression.
                boolVal = self.expr.run()



# A class that defines a PrintStatement object.
class PrintStatement:
    # Capture the expression value of a print statement in a PrintStatement object.
    def __init__(self, expr):
        self.expr = expr


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "PrintStatement({0})".format(repr(self.expr))


    # The string representation of the object.
    def __str__(self):
        return "print(" + str(self.expr) + ");"


    # Evaluate the PrintStatement object.
    def run(self):
        # Determine the value of the expression.
        value = self.expr.run()

        # Print the value of the expression.
        print(value)



# A class that represents a BinaryExpr object.
class BinaryExpr:
    # Initialize a dictionary for the binary operator tokens.
    binOperations = {lexer.Lexer.BOOLOR: '||', lexer.Lexer.BOOLAND: '&&', lexer.Lexer.EQ: '==', lexer.Lexer.NOTEQ: '!=',
     lexer.Lexer.LESS: '<', lexer.Lexer.LESSEQ: '<=', lexer.Lexer.GREAT: '>', lexer.Lexer.GREATEQ: '>=',
     lexer.Lexer.ADD: '+', lexer.Lexer.SUBTRACT: '-', lexer.Lexer.MULTIPLY: '*',lexer.Lexer.DIVIDE: '/',
     lexer.Lexer.REMAINDER: '%', lexer.Lexer.POWER: '**'}

    # Capture the operation and operands of a binary expression into a BinaryExpr object.
    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.op = op



    # Define functions needed to evaluate the BinaryExpr object.
    def boolOr(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 == 'true' or val2 == 'true':
            return 'true'

        else:
            return 'false'

    def boolAnd(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 == 'true' and val2 == 'true':
            return 'true'

        else:
            return 'false'

    def eqTo(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 == val2:
            return 'true'

        else:
            return 'false'

    def notEq(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 != val2:
            return 'true'

        else:
            return 'false'

    def lsThn(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 < val2:
            return 'true'

        else:
            return 'false'

    def lsEq(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 <= val2:
            return 'true'

        else:
            return 'false'

    def gtThn(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 > val2:
            return 'true'

        else:
            return 'false'

    def gtEq(self, left, right):
        # Evaluate the expressions to get their values for comparison.
        val1 = left.run()
        val2 = right.run()

        # Compare the values.
        if val1 >= val2:
            return 'true'

        else:
            return 'false'

    def add(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        return val1 + val2

    def subtract(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        return val1 - val2

    def multiply(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        return val1 * val2

    def divide(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        # Check whether integer division is required.
        if isinstance(val1, int) and isinstance(val2, int):
            return val1 // val2

        else:
            return val1 / val2

    def remainder(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        return val1 % val2

    def power(self, left, right):
        # Evaluate the expressions to get their values.
        val1 = left.run()
        val2 = right.run()

        return pow(val1, val2)

    # Initialize a dictionary of binary operator functions.
    binaryOp = {lexer.Lexer.BOOLOR:boolOr, lexer.Lexer.BOOLAND:boolAnd, lexer.Lexer.EQ:eqTo, lexer.Lexer.NOTEQ:notEq,
                lexer.Lexer.LESS:lsThn, lexer.Lexer.LESSEQ:lsEq, lexer.Lexer.GREAT:gtThn, lexer.Lexer.GREATEQ:gtEq,
                lexer.Lexer.ADD:add, lexer.Lexer.SUBTRACT:subtract, lexer.Lexer.MULTIPLY:multiply,
                lexer.Lexer.DIVIDE:divide, lexer.Lexer.REMAINDER:remainder, lexer.Lexer.POWER:power}


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "BinaryExpr({0},{1},{2})".format(self.op, repr(self.left), repr(self.right))


    # The string representation of the object.
    def __str__(self):
        return "({0} {1} {2})".format( str(self.left), str(BinaryExpr.binOperations[self.op]), str(self.right))


    # Evaluate the BinaryExpr object.
    def run(self):
        return BinaryExpr.binaryOp[self.op](self, self.left, self.right)



# A class that represents a UnaryExpr object.
class UnaryExpr:
    # Initialize a dictionary for the unary operator tokens.
    unaryOp = {lexer.Lexer.NOT:'!', lexer.Lexer.SUBTRACT:'-'}

    # Capture the optional operator and expression of a unary expression in a UnaryExpr object.
    def __init__(self, expr, op):
        self.expr = expr
        self.op = UnaryExpr.unaryOp[op]


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "UnaryExpr({0},{1})".format(repr(self.expr), repr(self.op))

    # The string representation of the object.
    def __str__(self):
        return "(" + str(self.op) + str(self.expr) + ")"


    # Evaluate the UnaryExpr object.
    def run(self):
        # Determine the value of the expression.
        value = self.expr.run()

        # Evaluation of a unary expression with operator '!'.
        if self.op == '!':
            if value == 'false' or value in ('', 0):
                return 'true'
            else:
                return 'false'

        # Evaluation of a unary expression with operator '-'.
        else:
            return -value



# A class that represents an IdExpr object.
class IdExpr:
    # Capture an identifier in the IdExpr object.
    def __init__(self, identify):
        self.id = identify


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "IdExpr({0})".format(self.id)

    # The string representation of the object.
    def __str__(self):
        return self.id


    # Evaluate the IdExpr object.
    def run(self):
        return Program.declarations[self.id][1]



# A  class that represents an LitExpr object.
class LitExpr:
    # Capture a literal's value (int, float, bool) in the LitExpr object.
    def __init__(self, litVal):
        self.value = litVal


    # A syntactically correct representation of the object that could be used to recreate it.
    def __repr__(self):
        return "LitExpr({0})".format(self.value)

    # The string representation of the object.
    def __str__(self):
        return str(self.value)


    # Evaluate the LitExpr object.
    def run(self):
        # A regular expression for a floating point number.
        float_patt = re.compile("^\d+\.\d+$|^[1-9]\.\d+e[-]?[1-9]\d*$")

        # Boolean literal.
        if self.value in ('true', 'false'):
            return self.value

        # Float literal.
        elif float_patt.fullmatch(self.value):
            return float(self.value)

        # Integer literal.
        else:
            return int(self.value)

