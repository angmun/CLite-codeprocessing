# Angelica Munyao
# Homework 6:
# Lexical Analyzer for CLite programs.

# We will need the regular expression library to make use of regular expressions in our code.
import re

# We will need the sys library to run the program in the terminal.
import sys

# We will need the os library to check whether the opened file is empty.
import os

class Lexer:
    """
    The Lexer class analyzes tokens in a CLite program.
    """

    # Counter generator.
    # NB// Using the @staticmethod decorator results in an error; 'staticmethod' objects are not callable.
    # Without it, the method works just fine.
    def __Counter():
        i = 0
        while True:  # Continue generating integer values (no StopIteration error).
            yield i
            i = i + 1

    # Constants that represent token classifiers.
    cnt = __Counter()  # Generator factory to generate representative indices for the token types.

    # Operator tokens:
    ADD = next(cnt)
    SUBTRACT = next(cnt)
    MULTIPLY = next(cnt)
    DIVIDE = next(cnt)
    REMAINDER = next(cnt)
    POWER = next(cnt)
    BOOLAND = next(cnt)
    BOOLOR = next(cnt)
    EQ = next(cnt)
    NOT = next(cnt)
    NOTEQ = next(cnt)
    LESS = next(cnt)
    LESSEQ = next(cnt)
    GREAT = next(cnt)
    GREATEQ = next(cnt)

    # Assignment token:
    ASSIGN = next(cnt)

    # Literal tokens:
    ID = next(cnt)
    INTLIT = next(cnt)
    FLOATLIT = next(cnt)
    STRINGLIT = next(cnt)
    COMMENT = next(cnt)

    # Keyword tokens:
    KWDIF = next(cnt)
    KWDELSE = next(cnt)
    KWDWHILE = next(cnt)
    KWDINT = next(cnt)
    KWDFLOAT = next(cnt)
    KWDBOOL = next(cnt)
    KWDTRUE = next(cnt)
    KWDFALSE = next(cnt)
    KWDPRINT = next(cnt)

    # Punctuation tokens:
    COMMA = next(cnt)
    SEMICOLON = next(cnt)
    CURLYLEFT = next(cnt)
    CURLYRIGHT = next(cnt)
    SQUARELEFT = next(cnt)
    SQUARERIGHT = next(cnt)
    PARENLEFT = next(cnt)
    PARENRIGHT = next(cnt)

    # Error / notification constants.
    EMPTYFILE = next(cnt)
    EOF = next(cnt)
    FILENOTFOUND = next(cnt)
    ILLEGALTOKEN = next(cnt)



    # Token dictionary. Contains operators, keywords, punctuation marks and the assignment token.
    td = {'+':(ADD, "Add"), '-':(SUBTRACT, "Subtract"), '*':(MULTIPLY, "Multiply"), '/':(DIVIDE, "Divide"), '%':(REMAINDER, "Remainder"), '**':(POWER, "Power"),
          '&&':(BOOLAND, "Boolean And"), '||':(BOOLOR, "Boolean Or"), '==':(EQ, "Equal"), '!':(NOT, "Not"), '!=':(NOTEQ, "Not Equal"),
          '<':(LESS, "Less Than"), '<=':(LESSEQ, "Less Than or Equal To"), '>':(GREAT, "Greater Than"), '>=':(GREATEQ, "Greater Than or Equal To"),
          '=': (ASSIGN, "Assign"),
          'if':(KWDIF, "Keyword If"), 'else':(KWDELSE, "Keyword Else"), 'while':(KWDWHILE, "Keyword While"), 'print':(KWDPRINT, "Keyword Print"),
          'int':(KWDINT, "Keyword Int"), 'float':(KWDFLOAT, "Keyword Float"), 'bool':(KWDBOOL, "Keyword Boolean"), 'true':(KWDTRUE, "Keyword True"),
          'false':(KWDFALSE, "Keyword False"), ',':(COMMA, "Comma"), ';':(SEMICOLON, "Semicolon"), '{':(CURLYLEFT, "Left Curly Bracket"),
          '}':(CURLYRIGHT, "Right Curly Bracket"), '[':(SQUARELEFT, "Left Square Bracket"),
          ']':(SQUARERIGHT, "Right Square Bracket"),'(':(PARENLEFT, "Left Parenthesis"), ')':(PARENRIGHT, "Right Parenthesis")}



    # Set up the regular expression for splitting the lines of the CLite code into tokens:
    split_patt = re.compile(
        """ # Triple quoted strings can cross line boundaries; verbose allows us to use them for the regular expression.
        (\".*\") | # strings between double quotes
        ([1-9]\.\d+e[-]?[1-9]\d*) | # floating point numbers in scientific notation
        (//) | # double forward slash for comments
        \s | # all whitespace
        (\+) | # operator +
        (-) | # operator -
        (\*\*) | # operator **
        (\*) | # operator *
        (/) | # operator /
        (%) | # operator %
        (&&) | # operator &&
        (\|\|) | # operator ||
        (!=) | # operator !=
        (!) | # operator !
        (==) | # operator ==
        (>=) | # operator >=
        (<=) | # operator <=
        (>) | # operator >
        (<) | # operator <
        (=) | # assignment
        ({) | # punctuation {
        (}) | # punctuation }
        (\[) | # punctuation [
        (\]) | # punctuation ]
        (\() | # punctuation (
        (\)) | # punctuation )
        (,) | # punctuation ,
        (;) # punctuation ;
""",
        re.VERBOSE
    )



    # Set up regular expressions used to match literal patterns:
    # Regular expression for an identifier. An identifier must begin with a letter or underscore and can be followed
    # by other letters, numbers or underscores.
    id_patt = re.compile("^[a-zA-Z_][a-zA-Z\d_]*$")

    # Regular expression for a string. A string can contain any character including a newline character
    # provided they are enclosed in double quotation marks.
    str_patt = re.compile("^[\"].*[\"]$", re.DOTALL)

    # Regular expression for an integer. An integer is a sequence of digits.
    int_patt = re.compile("^\d+$")

    # Regular expression for a floating point number. A real number consists of one or more digits followed
    # by a decimal point then one or more other digits afterwards. A real number could also be in scientific
    # notation, where the first digit is non-zero followed by a decimal point and one or more other digits
    # afterwards then ending with e and a sequence of digits where the first and last
    # digits are non-zero.
    float_patt = re.compile("^\d+\.\d+$|^[1-9]\.\d+e[-]?[1-9]\d*$")



    # Generate tokens from a given file.
    def token_generator(self, filename):
        # Consider what could go wrong with opening the file given a filename:

        # Error: The given filename cannot be found in the system and cannot be opened.
        try:
            file = open(filename,'r')

        except IOError:
            yield (Lexer.FILENOTFOUND, "File Not Found", filename, "N/A")
            exit("Error: The given file name cannot be found in the system. File cannot be opened.")


        # Check whether the file is empty.
        if os.stat(filename).st_size != 0:
            # File was successfully opened and is non-empty. We can read through it.

            # Create a variable to keep track of the line number.
            linenum = 1

            for line in file:
                # Split the line into possible tokens for assessment.
                tokens = Lexer.split_patt.split(line)

                # Take out any spaces and empty strings in the resulting list of possible tokens.
                tokens = [t for t in tokens if t]

                for t in tokens:
                    # Check for operators, keywords and punctuation.
                    if t in Lexer.td:
                        # Yield the type and token as a pair.
                        yield (Lexer.td[t][0], Lexer.td[t][1], t, linenum)

                    # Check for identifiers.
                    elif Lexer.id_patt.search(t):
                        # Yield the type and identifier as a pair.
                        yield (Lexer.ID, "Identifier", t, linenum)

                    # Check for strings.
                    elif Lexer.str_patt.search(t):
                        # Yield the type and string as a pair.
                        yield (Lexer.STRINGLIT, "String Literal", t, linenum)

                    # Check for floating point numbers.
                    elif Lexer.float_patt.search(t):
                        # Yield the type and string as a pair.
                        yield (Lexer.FLOATLIT, "Floating Point Literal", t, linenum)

                    # Check for integers.
                    elif Lexer.int_patt.search(t):
                        # Yield the type and string as a pair.
                        yield (Lexer.INTLIT, "Integer Literal", t, linenum)

                    # Check for comments.
                    elif t == '//':
                        # Move to the next line of the file by exiting the token loop of the current line.
                        break

                    # Error: The token is not defined.
                    else:
                        # Yield the ILLEGALTOKEN type.
                        yield (Lexer.ILLEGALTOKEN, "Illegal Token", t, linenum)

                        # Exit the program as an illegal token was found.
                        # exit("Error: Illegal token \"" + t + "\" encountered at line number " + str(linenum) + ".")

                # Update the line number after going through a line.
                linenum += 1

            # This is the end of the file; the last line has been read.
            yield (Lexer.EOF, "End of File", "End of File", linenum - 1)

            # Close the file once it has been completely read through.
            file.close()

        # Error: The file is empty.
        else:
            yield (Lexer.EMPTYFILE, "Empty File", "Empty File", "N/A")
            exit("Error: The file is empty. There are no tokens to process.")

# Test main.
if __name__ == '__main__':

    # Check whether a file name has been given.
    # Error: A file name was not given.
    if (len(sys.argv) < 2):
        exit("Error: No file name given. Please input a file name to open and process.")

    else:
        # Create a Lexer object.
        lex = Lexer()

        # Create a token generator from the Lexer object.
        tg = lex.token_generator(sys.argv[1])

        # Set up a neat output format for token printing.
        print("%-25s%-20s%-15s"%("Token", "Name", "Line number"))
        print("_"*60)
        while True:
            try:
                tok = next(tg)
                print("%-25s%-20s%-15s"%(tok[1], tok[2], tok[3]))

            # All possible tokens have been yielded at this point. Break from the loop.
            except StopIteration:
                break
