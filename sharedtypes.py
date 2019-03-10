
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
