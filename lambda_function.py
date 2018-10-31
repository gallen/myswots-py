from myswots import *
from swotsquestion import *
from swotsquiz import *
from sessionattrs import *
import io
import json


USER_ID = 19484
SKILL_ID = 55 #cricket
#SKILL_ID = 52 # English speaking
TOPICS = [2125, 2127, 2129, 2131]
#TOPICS = [1992, 1924, 1926, 2299, 2301, 2315, 1912, 1930]
QUIZ_DURATION = 20 # MINUTES
QUESTION_COUNT = 5
#SKILL_NAME = "baseball"

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

    if intentName == "AMAZON.YesIntent":
        return handleYes(session)
    elif intentName == "AMAZON.NoIntent":
        return handleNo(session)
    elif intentName == "AMAZON.HelpIntent":
        return getWelcomeResponse(session)
    elif intentName == "AMAZON.FallbackIntent":
        return handleFallback(session)      
    elif intentName == "AMAZON.CancelIntent" or intentName == "AMAZON.StopIntent":
        return handleSessionEndRequest(session)
    elif intentName == "AnswerIntent":
        answer = int(intentRequest["intent"]["slots"]["answer"]["value"])
        return handleAnswer(session, answer)
    else:
        raise ValueError("Invalid intent")

def endSwots(session):
    sa = SessionAttrs(attrs = session["attributes"])
    if sa.attrs['userId']:
        swots = MySwots(sa.attrs['userId'])
        swots.finishQuiz(sa.attrs['testId'])

# End session handler
def handleSessionEndRequest(session):
    message = "Thank you for using my swots skill.  See you next time!"

    return buildResponse(message, shouldEndSession=True)

# Welcome hanlder
def getWelcomeResponse(session):  
    message = "Welcome to my swots quiz game. " \
                    "I will ask you " + str(QUESTION_COUNT) + " questions, " \
                    "try to answer as many right as you can. Just say the number of the answer. " \
                    "Are you ready?"
    reprompt = "Are you ready? Please say yes or no." 
    return buildResponse(message, reprompt=reprompt, sessionAttributes=session['attributes'])

# fallback handler
def handleFallback(session):     
    message = "See you next time."
    return buildResponse(message, sessionAttributes=session['attributes'], shouldEndSession=True)

# Yes Intent hanlder
def handleYes(session):
    sa = SessionAttrs(attrs = session["attributes"])
    if sa.attrs['cur'] != 0:
        return handleFallback(session)
    else: # first question
        q = loadQuestion(sa)
        message = buildQSpeaklet(q, 0)
        #sa.attrs['answer'] = q.answer
        #sa.attrs['answerText'] = q.options[sa.attrs['answer'] - 1]
        #sa.attrs['solution']  = q.solution        
        reprompt = "Please say an option."
        return buildResponse(message, reprompt, True, sessionAttributes=sa.attrs)
        
 

# No intent hanlder
def handleNo(session):
    return handleSessionEndRequest(session)


def handleAnswer(session, answer):
    sa = SessionAttrs(attrs=session["attributes"])
    if sa.isLast():
        a = loadAnswer(sa, answer)
        message = buildLastAnswerSpeaklet(sa, a)
        return buildResponse(message, "", True, shouldEndSession = True, sessionAttributes=sa.attrs)
    else:
        sa.next()
        q = loadQuestion(sa)
        a = loadAnswer(sa, answer)
        message = buildAnswerSpeaklet(sa, a, q)
        sa.attrs['answer'] = q.answer
        sa.attrs['answerText'] = q.options[sa.attrs['answer'] - 1]
        sa.attrs['solution']  = q.solution
        reprompt = "Please say an option."
        return buildResponse(message, reprompt, True, sessionAttributes=sa.attrs)

def loadQuestion(sa):
    index = sa.attrs["cur"]
    swots = MySwots(sa.attrs['userId'])
    quiz = swots.loadQuiz(sa.attrs['testId'])
    question = quiz.loadQuestion(sa.attrs['questions'][index])
    return question   

def loadAnswer(sa, answer):
    index = sa.attrs["cur"]
    qId = sa.attrs['questions'][index]
    testId = sa.attrs['testId']
    swots = MySwots(sa.attrs['userId'])
    return swots.getAnswer(testId, qId, answer)
    
#----------------------------

def buildQSpeaklet(q, index):
    ret = io.StringIO("")
    startSpeaklet(ret)
    addParagraph(ret, "Question " + str(index + 1) + ": " + q.question)
    for i in range(len(q.options)):
        addSentence(ret, "Option " + str(i + 1) +  ": " + q.options[i])
    endSpeaklet(ret)
    return ret.getvalue()

def buildAnswerSpeaklet(sa, answer, nextq):
    ret = io.StringIO("")
    startSpeaklet(ret)    
    if answer.status != "Wrong":
        addParagraph(ret, "Correct.")
        sa.correct()
    else:
        addParagraph(ret, "The correct answer is " + str(answer.answer) + ": " + answer.answerText)
    if answer.solution != "":
        addSentence(ret, "Explanation: " + answer.solution)
    addSentence(ret, "Your score is " + str(sa.attrs['correct']))

    index = sa.attrs['cur']
    q = nextq
    addParagraph(ret, "Question " + str(index + 1) + ": " + q.question)
    for i in range(len(q.options)):
        addSentence(ret, "Option "  + str(i + 1) +  ": " + q.options[i])
    endSpeaklet(ret) 
    return ret.getvalue()   

def buildLastAnswerSpeaklet(sa, answer):
    ret = io.StringIO("")
    startSpeaklet(ret)    
    if answer.status != "Wrong":
        addParagraph(ret, "Correct.")
        sa.correct()
    else:
        addParagraph(ret, "The correct answer is " + str(answer.answer) + ": " + answer.answerText)
    if answer.solution != "":
        addSentence(ret, "Explanation: " + answer.solution)
    addSentence(ret, "Your final score is " + str(sa.attrs['correct']))
    addParagraph(ret, "Thanks for playing. See you next time")
    endSpeaklet(ret) 
    return ret.getvalue()      

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
