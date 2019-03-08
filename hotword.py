#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import argparse
import json
import os.path
import pathlib2 as pathlib
import RPi.GPIO as GPIO
import google.oauth2.credentials
import time

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


WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""
def checkdist():
	GPIO.output(26, GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(26, GPIO.LOW)
	while not GPIO.input(19):
		pass
	t1 = time.time()
	while GPIO.input(19):
		pass
	t2 = time.time()
	return (t2-t1)*340/2

def setunsetpin(pin, delay):
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(pin, GPIO.LOW)


def process_event(event):

    
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))
            steps = 1

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

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(19, GPIO.IN)

    #now i am going to calculate the distance
    distToObstacle = checkdist()

    print('Distance to obstacle', distToObstacle)
    #setunsetpin(18, .5)

    distToObstacle = checkdist()

    print('Distance to obstacle', distToObstacle)
    
    device_config_file = os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        )
    credentials_file = os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        )
    with open(credentials_file, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = "mypi-f33e7-product"
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
    should_register = ("mypi-f33e7-product" != device_model_id)

    with Assistant(credentials, device_model_id) as assistant:
        events = assistant.start()

        device_id = assistant.device_id
        print('device_model_id:', device_model_id)
        print('device_id:', device_id + '\n')

        # Re-register if "device_id" is different from the last "device_id":
        if should_register or (device_id != last_device_id):
            register_device("mypi-f33e7", credentials,
                                device_model_id, device_id, "")
                pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                    exist_ok=True)
                with open(args.device_config, 'w') as f:
                    json.dump({
                        'last_device_id': device_id,
                        'model_id': device_model_id,
                    }, f)
            else:
                print(WARNING_NOT_REGISTERED)

        for event in events:
            if event.type == EventType.ON_START_FINISHED:
                assistant.send_text_query(args.query)
        
            process_event(event)

    GPIO.cleanup()

if __name__ == '__main__':
    main()
