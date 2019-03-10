import elements
import scanner
import robotmover
import commands
import command 

element_data = elements.Elements()
mover = robotmover.Mover()
commandRetriever = commands.CommandRetriever(commandProcessor)
maxAdjustAttempt = 1

#print(scanner.scanElement())
def commandProcessor(command):
    print("next command" , command)
    mover.move(command.direction, command.steps)

def start():
    scannedElement = scanner.scanElement(element_data)
    if(scannedElement != None):
        print("Found element: =>")
        print(scannedElement)

    print("generate and process voice commands")
    nextCommand = commandRetriever.generateAndProcessCommands()
    
    #    adjustAttempt = maxAdjustAttempt
    #    print("Scanning")
    #    scannedElement = scanner.scanElement(element_data)
    #    while(adjustAttempt > 0):
    #        if(scannedElement == None):
    #            print("No element found")
    #            scannedElement = scanner.scanElement(element_data)
    #            adjustAttempt -= 1
    #            mover.adjust()
    #        else:
    #            break

    #    if(scannedElement != None):
    #        print("Found element: =>")
    #        print(scannedElement)
    

start()