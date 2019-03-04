import csv

class Element:
    def __init__(self, atomicNumber, symbol, name):
        self.atomicNumber = atomicNumber
        self.symbol = symbol
        self.name = name

    def __str__(self):
        return self.atomicNumber + " => " + self.symbol + "  => " + self.name

class Elements:
    element_data = []

    def __init__(self):
        with open('elements.csv') as f:
            reader = csv.reader(f)
            line = 0
            for row in reader:
                if(line == 0):
                    line += 1
                else:
                    self.element_data.append(Element(row[0], row[1].strip(), row[2].strip()))
                    #print(row)

    def findElementBySymbol(self, identifier):
        for element in self.element_data:
            if(element.symbol.lower() == identifier.lower()):
                return element
        return

    def findElementByText(self, identifier):
        for element in self.element_data:
            if(element.name.lower() == identifier.lower()):
                return element
        return

    def findElementByMatch(self, identifier):
        for element in self.element_data:
            if(identifier.lower() in element.name.lower()):
                return element
        return