from enum import Enum 
from time import sleep

class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2
    RIGHTFORWARD = 3
    LEFTFORWARD = 4
    RIGHTBACKWARD = 5
    LEFTBACKWARD = 6

class Command:
    def __init__ (self, direction, steps = 0):
        self.direction = direction
        self.steps = steps

class CommandRetriever:
    firstCall = True
    iteration = 0

    def getCommand(self):
        if(self.firstCall):
            self.firstCall = False
        else:
            sleep(.5)

        self.iteration += 1
        if(self.iteration == 1):
            return Command(Direction.FORWARD, 1)
        if(self.iteration == 2):
            return Command(Direction.BACKWARD, 1)
        if(self.iteration == 3):
            return Command(Direction.LEFTBACKWARD, 1)
        if(self.iteration == 4):
            return Command(Direction.RIGHTFORWARD, 1)
        if(self.iteration == 5):
            return Command(Direction.LEFTFORWARD, 1)
        if(self.iteration == 6):
            return Command(Direction.RIGHTBACKWARD, 1)