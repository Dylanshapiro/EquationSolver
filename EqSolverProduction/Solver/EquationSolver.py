'''
This object utilizes faster rcnn object detection model, trained on mathematical symbols
0-9,+,-,/,x,(, and )

Pass a filepath to the solve method
'''

from Utilities.Image import EqSolImage
from ObjectDetectionModule.SymbolDetector import SymbolDetector
from Utilities.imageToEquationParser import ImageToEquationParser
import cv2

class CVES:
    def __init__(self):
        self.SymbolDetector = SymbolDetector(
            '../ObjectDetectionModule/model/inference_graph',
            '../ObjectDetectionModule/model/labelmap.pbtxt',
            17
        )
        self.imageToEquationParser = ImageToEquationParser()

    '''
    Solves the equation presented in a given image
    '''
    def solve(self, file, debug=0):
        # Read in image
        if debug >= 1:
            print("Reading Image")
        image = EqSolImage(filePath=file)
        image.resize(1024,1024)

        # Find Bounding Boxes
        if debug >= 1:
            print("Boxing Objects")
        # Boxes image
        boxes, image = self.SymbolDetector.box(image)

        boxesToFormat = []
        for box in boxes:
            boxesToFormat.append(box.boxAsTL_BR_L())
        # Save boxed imaged
        boxedFile=file[:-4]+"_boxed"+file[-4:]
        cv2.imwrite(boxedFile, image)

        tempEquationAsString = self.imageToEquationParser.boxesToString(boxesToFormat)
        equationAsString, answer = self.imageToEquationParser.equationStringToAnswer(tempEquationAsString)

        return equationAsString, answer




