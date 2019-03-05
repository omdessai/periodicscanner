import requests
import io
import json
import elements
from time import sleep
from picamera import PiCamera

subscription_key = "222d05cd325541c99da0f2e96ada9eca"
ocr_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/ocr"

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
params  = {'language': 'unk', 'detectOrientation': 'true'}

attempts = 1
camera = PiCamera()

def scanElement(element_data):
    attempt = attempts
    while(attempt > 0):
        attempt -= 1
        scannedwords = scanElementAttempt()
        if(scannedwords != None):
            for word in scannedwords:
                scannedElement = element_data.findElementBySymbol(word)
                if(scannedElement != None):
                    return scannedElement
            for word in scannedwords:
                scannedElement = element_data.findElementByText(word)
                if(scannedElement != None):
                    return scannedElement
            for word in scannedwords:
                scannedElement = element_data.findElementByMatch(word)
                if(scannedElement != None):
                    return scannedElement
        sleep(.2)#we will try again to scan

def scanElementAttempt():
    stream = io.BytesIO()
    
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
    #print("analysis=>")
    #print(analysis)
    # Extract the word text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info["text"])
    word_infos.sort()#sort so that symbols will be before the longer names
    #print("Printing scanned words")
    #print(word_infos)
    return word_infos


#scanElement(elements.Elements())