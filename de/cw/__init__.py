import logging
import json
import time
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rt42Sign = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Kreisintegral', '\xc3\x84', '\xc3\x96', '\xc3\x9c', '\xc3\x9f', '@' ]

def buildResponse(output):
    return {
        'version': '1.0',
        'response': {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        
        'shouldEndSession': True
    }}
    
def getRt42TimeDigits(time):
    digits = 0
    while pow(42, digits) <= time + 1:
        digits += 1
    return digits
    
def getRt42Time():
    rt42Time = ""
    currentTime = time.time() - 943016400
    digits = getRt42TimeDigits(currentTime)
    logger.info(digits)
    for index in range(digits - 1, -1, -1):
        rt42Time += rt42Sign[int(currentTime / pow(42, index))] + " "
        currentTime = currentTime % pow(42, index)
        logger.info(index)
    return rt42Time

def getNextRtEvening():
    date = datetime.datetime.now()
    daysAhead = 3 - date.weekday()
    if daysAhead <= 0: # Target day already happened this week
        daysAhead += 7
    date = date + datetime.timedelta(daysAhead)
    logger.info(date)
    return date.strftime("%d.%m.%Y")

def rt(event, context):
    logger.info('got event{}'.format(event))
    if(event['request']['intent']['name'] == 'RtTimeIntent'):
        return buildResponse("Die aktuelle Uhrzeit lautet " + getRt42Time())
    elif(event['request']['intent']['name'] == 'RtNextThursdayIntent'): 
        return buildResponse("Der n\xc3\xa4chste r t Abend ist am " + getNextRtEvening())
    else:
        return buildResponse("Deine Anfrage f\xc3\xbchrt ins Nichts.")