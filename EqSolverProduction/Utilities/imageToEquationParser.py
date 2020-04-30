'''
Solves an equation as boxed symbols from an image
'''

from Utilities.box import Box

class ImageToEquationParser:
    def __init__(self):
        self.numericSymbols = ["0","1","2","3","4","5","6","7","8","9"]
        self.operators = ["+", "-", "/", "*"]
        self.parens = ["(", ")"]
        # Needed for converting some special symbols
        self.specialSymbols = {
            "Loop 2": "2",
            "x": "*"
        }

    '''
    Solves an equation string
    '''
    def equationStringToAnswer(self, eqString, useParenthesisCorrection=True):

        finalEquation = ""
        tokens = eqString.split(' ')

        # Some simple logic that corrects for parenthesis
        if useParenthesisCorrection:
            paren = 0
            for tok in tokens:
                if tok == "(":
                    paren += 1
                elif tok == ")":
                    paren -= 1

            if paren > 1:
                for tok in reversed(range(len(tokens))):
                    if tokens[tok] == "(":
                        ind = tok
                        break
                tokens[ind] = ")"
            elif paren < -1:
                for tok in range(len(tokens)):
                    if tokens[tok] == ")":
                        ind = tok
                        break
                tokens[ind] = "("
            elif paren == -1:
                tokens.insert(0, "(")
            elif paren == 1:
                tokens.append(")")

            for token in tokens:
                if token in self.operators:
                    finalEquation += " " + token + " "
                else:
                    finalEquation += token


        # Evaluate the equation
        try:
            solution = str(eval(finalEquation))
        except:
            solution = "Failed to understand"

        return finalEquation, solution

    '''
    Converts boxes of equation to a string with each token seperated by a space ' '
    '''
    def boxesToString(self, boxes):
        # Read in boxes to Box objects
        boxesToSort = []
        for box in boxes:
            tempBox = Box([box[0], box[1]], method="ptAndPt", label=box[2])
            boxesToSort.append(tempBox)

        # Bubble sort, no need to over-engineer for a small array
        n = len(boxesToSort)
        swapped = True
        x = -1
        while swapped:
            swapped = False
            x = x + 1
            for i in range(1, n - x):
                if boxesToSort[i - 1].getBRX() > boxesToSort[i].getBRX():
                    boxesToSort[i - 1], boxesToSort[i] = boxesToSort[i], boxesToSort[i - 1]
                    swapped = True

        # Build string with spaces separating tokens
        equationString = ""
        for box in boxesToSort:
            label = box.getLabel()
            # Check for special symbol
            if label in self.specialSymbols.keys():
                label = self.specialSymbols[label]
            equationString += label + " "

        return equationString[:-1]
