from myswots import *
from swotsquestion import *
from swotsquiz import *
from sessionattrs import *
import json


USER_ID = 19484
SKILL_ID = 55
TOPICS = [2125, 2127, 2129, 2131]
QUIZ_DURATION = 10 # MINUTES
QUESTION_COUNT = 5
SKILL_NAME = "baseball"

# lambda entry point function.
# event is alex skill input
def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return onLaunch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return onIntent(event["request"], event["session"])

# Laurch request handler
def onLaunch(launchRequest, session):
    # create quiz
    swots = MySwots(USER_ID)
    quiz = swots.createQuiz(SKILL_ID, QUESTION_COUNT, TOPICS, QUIZ_DURATION)
    sa = SessionAttrs(quiz)
    session['attributes'] = sa.attrs
  
    return getWelcomeResponse(session)

# Intent request handler
def onIntent(intentRequest, session):
    #intent = intentRequest["intent"]
    intentName = intentRequest["intent"]["name"]
    if 'attributes' not in session:
        session['attributes'] = {}

    elif intentName == "AMAZON.HelpIntent":
        return getWelcomeResponse(session)
    elif intentName == "AMAZON.FallbackIntent":
        return handleFallback(session)      
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest(session)
    else:
        raise ValueError("Invalid intent")

# End session handler
def handleSessionEndRequest(session):
    message = "Thank you for using malboro public school skill.  See you next time!"

    return buildResponse(message, shouldEndSession=True)

# Welcome hanlder
def getWelcomeResponse(session):
    swots = MySwots(USER_ID)
    quiz = swots.createQuiz(55, 5, [2125, 2127, 2129, 2131], 10)
    
    message = "Welcome to my swots skill. " \
                    "There're " + str(QUESTION_COUNT) + " " + SKILL_NAME + " questions "\
                    "for you to answer, are you ready?"
    reprompt = "Are you ready? Please say yes or no." 
    return buildResponse(message, reprompt=reprompt, sessionAttributes=session['attributes'])

# fallback handler
def handleFallback(session):
    message = "I don't know that. Please say the option you chose."
    return buildResponse(message, sessionAttributes=session['attributes'])



# No intent hanlder
def handleNo(session):
    return handleSessionEndRequest(session)

#----------------------------
# Session handling
def shouldEnd(session):
    return 'newsDelivered' in session['attributes'] and 'eventsDelivered' in session['attributes']
#----------------------------


#----------------------------
# speaklet helper routines

def startSpeaklet(stringIO):
    stringIO.write('<speak>')

def endSpeaklet(stringIO):
    stringIO.write("</speak>")

def addParagraph(stringIO, message):
    stringIO.write("<p>")
    stringIO.write(message)
    stringIO.write("</p>")

def addSentence(stringIO, message):
    stringIO.write("<s>")
    stringIO.write(message)
    stringIO.write("</s>")

def addSpeechcon(stringIO, speeckcon):
    stringIO.write('<say-as interpret-as="interjection">')
    stringIO.write(speeckcon)
    stringIO.write("</say-as>") 

def createSimpleSpeaklet(message):
    return "<speak>" + message + "</speak>"
#-------------------------------

    

# build alexa skill response
def buildResponse(message, reprompt = "", isSpeaklet=False, shouldEndSession = False, sessionAttributes = {}):
    ret = {
        'version': '1.0',
        "sessionAttributes": sessionAttributes,        
        'response': {
            'outputSpeech': {},
            "reprompt": {
                    "outputSpeech": {}
                },            
            'shouldEndSession': shouldEndSession            
        }
    }

    if isSpeaklet:
        ret['response']['outputSpeech']['type'] = "SSML"
        ret['response']['outputSpeech']['ssml'] = message  
        ret['response']['reprompt']['outputSpeech']['type'] = "SSML"
        ret['response']['reprompt']['outputSpeech']['ssml'] = createSimpleSpeaklet(reprompt)              
    else:
        ret['response']['outputSpeech']['type'] = "PlainText"
        ret['response']['outputSpeech']['text'] = message  
        ret['response']['reprompt']['outputSpeech']['type'] = "PlainText"
        ret['response']['reprompt']['outputSpeech']['text'] = reprompt                 

    return ret
