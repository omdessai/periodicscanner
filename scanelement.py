import requests
import io
import json
from time import sleep
from picamera import PiCamera

subscription_key = "222d05cd325541c99da0f2e96ada9eca"
ocr_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/ocr"

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
params  = {'language': 'unk', 'detectOrientation': 'true'}

attempts = 3


stream = io.BytesIO()
camera = PiCamera()
camera.resolution = (400, 400)
camera.start_preview()
sleep(2)
camera.capture(stream, format='jpeg')
stream.seek(0)
image_data = stream.getvalue()
stream.close()


response = requests.post(
    ocr_url, headers=headers, params=params, data=image_data)
response.raise_for_status()
analysis = response.json()
print(analysis)

print(analysis["language"])

print(analysis["regions"])
print(len(analysis["regions"]))

