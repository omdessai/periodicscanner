#!/usr/bin/env python

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

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError



def process_event(event):

    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))
            if command == "com.example.commands.MoveCar":
                if params['number'] != None:
                    steps = params['number']
                if params['direction1'] == 'RIGHT':
                    if params['direction2'] == 'FORWARD':
                        print("right forward by "+ steps)
                    else:
                        print("right by "+ steps)
                if params['direction1'] == 'LEFT':
                    if params['direction2'] == 'FORWARD':
                        print("left forward by "+ steps)
                    else:
                        print("left by "+ steps)
                if params['direction1'] == 'FORWARD':
                    if params['direction2'] == 'RIGHT':
                        print("right forward by "+ steps)
                    else:
                        print("forward by "+ steps)
                if params['direction1'] == 'BACKWARD':
                    if params['direction2'] == 'RIGHT':
                        print("right backward by "+ steps)
                    else:
                        print("backward by "+ steps)

def main():
    project_device_model_id = "mypi-f33e7-product"
    device_config_file = default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        )
    creds_file = default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        )
    with open(creds_file, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = None
    last_device_id = None
    try:
        with open(device_config_file) as f:
            device_config = json.load(f)
            device_model_id = device_config['model_id']
            last_device_id = device_config.get('last_device_id', None)
    except FileNotFoundError:
        pass

    # Re-register if "device_model_id" is given by the user and it differs
    # from what we previously registered with.
    should_register = (project_device_model_id != device_model_id)

    device_model_id = project_device_model_id or device_model_id

    with Assistant(credentials, project_device_model_id) as assistant:
        events = assistant.start()

        device_id = assistant.device_id
        print('device_model_id:', device_model_id)
        print('device_id:', device_id + '\n')

        for event in events:
            if event.type == EventType.ON_START_FINISHED:
                assistant.send_text_query("what is your name")
        
            process_event(event)

if __name__ == '__main__':
    main()
