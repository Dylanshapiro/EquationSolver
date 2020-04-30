'''
For data storage regarding boxes in an image
'''

class Box:
    def __init__(self, rect, method="relative", label=None):
        if method == "relative":
            self.TLx = rect[0]
            self.TLy = rect[1]
            self.BRx = rect[0] + rect[2]
            self.BRy = rect[1] + rect[3]
        elif method == "fixed":
            self.TLx = rect[0]
            self.TLy = rect[1]
            self.BRx = rect[2]
            self.BRy = rect[3]
        elif method == "ptAndPt":
            self.TLx = rect[0][0]
            self.TLy = rect[0][1]
            self.BRx = rect[1][0]
            self.BRy = rect[1][1]
            self.label = label
        self.label = label

    def getBRX(self):
        return self.BRx

    def getBRY(self):
        return self.BRy

    def boxAsTL_BR_L(self):
        return [[self.TLx, self.TLy], [self.BRx, self.BRy], self.label]

    def getLabel(self):
        return self.label

    def width(self):
        return self.BRx - self.TLx

    def height(self):
        return self.BRy - self.TLy

    def area(self):
        return (self.BRx - self.TLx) * (self.BRy - self.TLy)

    def __str__(self):
        return "[[{TLx}, {TLy}], [{BRx}, {BRy}]], {label}".format(TLx=self.TLx, TLy=self.TLy, BRx=self.BRx, BRy=self.BRy, label=self.label)