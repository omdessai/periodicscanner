import elements
import scanner

import commands
import robotmover

element_data = elements.Elements()
maxAdjustAttempt = 3

def scanAdjustAndScan():
    print("Scanning")
    scannedElement = scanner.scanElement(element_data)
    if(scannedElement != None):
        print("Found element: =>")
        print(scannedElement)
        return

    print("Element not determined, adjusting")
    adjustAttempt = maxAdjustAttempt
    while(adjustAttempt > 0):
        if(scannedElement == None):
            robomover.adjust()
            scannedElement = scanner.scanElement(element_data)
            adjustAttempt -= 1
        else:
            break

    if(scannedElement != None):
        print("Found element: =>")
        print(scannedElement)
        return

def start():
    scanAdjustAndScan()

    print("generate and process voice commands")
    nextCommand = commandRetriever.generateAndProcessCommands()

robomover = robotmover.Mover(scanAdjustAndScan)
commandRetriever = commands.CommandRetriever(robomover)

start()
