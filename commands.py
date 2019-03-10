from enum import Enum 
from time import sleep

import robotmover
import json
import os.path
import pathlib2 as pathlib
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

import faulthandler
faulthandler.enable()


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


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

class CommandRetriever:
    firstCall = True
    iteration = 0
    project_device_model_id = "mypi-f33e7-product"
    
    def __init__ (self):
        self.mover = robotmover.Mover()
        device_config_file = default=os.path.join(os.path.expanduser('~/.config'),'googlesamples-assistant','device_config_library.json')
        creds_file = default=os.path.join(os.path.expanduser('~/.config'),'google-oauthlib-tool','credentials.json')
        with open(creds_file, 'r') as f:
            self.credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))

        self.device_model_id = None
        try:
            with open(device_config_file) as f:
                device_config = json.load(f)
                self.device_model_id = device_config['model_id']
        except FileNotFoundError:
            pass

        self.device_model_id = self.project_device_model_id or self.device_model_id

    def process_event(self, event):
        print(event)
        if event.type == EventType.ON_DEVICE_ACTION:
            for command, params in event.actions:
                print('Do command', command, 'with params', str(params))
                if command == "com.example.commands.MoveCar":
                    steps = 1
                    if params['number'] != None:
                        steps = int(params['number'])
                        if(steps > 5):
                            steps = 5
                    if params['direction1'] == 'RIGHT':
                        if(params['direction2'] == None):
                            return
                        if params['direction2'] == 'FORWARD':
                            self.mover.move(Direction.RIGHTFORWARD, steps)
                        else:
                            self.mover.move(Direction.RIGHTBACKWARD, steps)
                    if params['direction1'] == 'LEFT':
                        if(params['direction2'] == None):
                            return
                        if params['direction2'] == 'FORWARD':
                            self.mover.move(Direction.LEFTFORWARD, steps)
                        else:
                            self.mover.move(Direction.LEFTBACKWARD, steps)
                    if params['direction1'] == 'FORWARD':
                        if(params['direction2'] == None):
                            self.mover.move(Direction.FORWARD, steps)
                        if params['direction2'] == 'LEFT':
                            self.mover.move(Direction.LEFTFORWARD, steps)
                        else:
                            self.mover.move(Direction.RIGHTFORWARD, steps)
                    if params['direction1'] == 'BACKWARD':
                        if(params['direction2'] == None):
                            self.mover.move(Direction.BACKWARD, steps)
                        if params['direction2'] == 'LEFT':
                            self.mover.move(Direction.LEFTBACKWARD, steps)
                        else:
                            self.mover.move(Direction.LEFTBACKWARD, steps)


    def generateAndProcessCommands (self):
        with Assistant(self.credentials, self.project_device_model_id) as assistant:
            events = assistant.start()
            device_id = assistant.device_id
            #print('device_model_id:', device_model_id)
            #print('device_id:', device_id + '\n')
            print("started assistant - will wait and process events")
            for event in events:
                if event.type == EventType.ON_START_FINISHED:
                    assistant.send_text_query("what is your name")
            
                self.process_event(event)

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
