import elements
import scanner
import robotmover
import commands

#print(scanner.scanElement())

def start():
    element_data = elements.Elements()
    mover = robotmover.Mover()
    commandRetriever = commands.CommandRetriever()
    maxAdjustAttempt = 3

    while True:
        scannedElement = scanner.scanElement(element_data)
        if(scannedElement != None):
            print("Found element: =>")
            print(scannedElement)
            
        print("getting next command")
        nextCommand = commandRetriever.getCommand()
        print("Next command => moving")
        mover.move(nextCommand.direction, nextCommand.steps)

        adjustAttempt = maxAdjustAttempt
        print("Scanning")
        scannedElement = scanner.scanElement(element_data)
        while(adjustAttempt > 0):
            if(scannedElement == None):
                print("No element found")
                scannedElement = scanner.scanElement(element_data)
                adjustAttempt -= 1
                mover.adjust()
            else:
                break

        if(scannedElement != None):
            print("Found element: =>")
            print(scannedElement)


start()