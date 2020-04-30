import cv2 as cv

class EqSolImage:
    '''
    Read in image, either pixels or file
    '''
    def __init__(self, file=None, filePath=None, pixels=None):
        if not file is None:
            self.pixels = cv.imread(file.read())
        elif not filePath is None:
            self.pixels = cv.imread(filePath)
        elif not pixels is None:
            self.pixels = pixels

    '''
    Blurs image with given blurTuple
    
    Ex image.blur((10,10))
    '''
    def blur(self, blurTuple):
        self.pixels = cv.blur(self.pixels, blurTuple)

    '''
    Resizes image to given width and height
    '''
    def resize(self, width, height):
        self.pixels = cv.resize(self.pixels, (width, height), interpolation=cv.INTER_AREA)

    def getSubImage(self,x1,x2,y1,y2):
        return EqSolImage(pixels=self.pixels[y1:y2, x1:x2])

    def getPixels(self):
        return self.pixels

    def getSize(self, type="dict"):
        pixShape = self.pixels.shape
        if type == "tuple":
            return pixShape
        elif type == "dict":
            return {"height": self.pixels.shape[0], "width": self.pixels.shape[1]}
