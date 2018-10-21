'''
Python SDK for myswots.com api.

Code flow to use this:
1. Create MySwots instance.
2. Create or load Quiz
3. Load questions and answers

e.g. check 'Unit test' section

'''

import requests
import swotsquiz
from swotsquestion import *


# myswots sdk main class.
class MySwots:
    API_ENTRY = "https://myswots.com/api/"
    # Constructor
    def __init__(self, userId):
        self._userId = userId

    # Create test    
    def createQuiz(self, skillId, noOfQuestions, topics, duration):
        apiComponent = "quiz/users/" + str(self._userId) + "/tests"
        payload = {"skillId": skillId,
                "noOfQuestions": noOfQuestions,
                "duration": duration,
                "tags": topics
            }
        quiz = self.postJson(apiComponent, payload)
        return swotsquiz.SwotsQuiz(quiz, self)
        
    @property
    def apiEntry(self):
        return MySwots.API_ENTRY

    @property
    def userId(self):
        return self._userId

    # Load existing Quiz with quiz ID
    def loadQuiz(self, quizId):
        apiComponent = "quiz/users/" + str(self._userId) + "/tests/" + str(quizId)
        quiz = self.getJson(apiComponent)
        return swotsquiz.SwotsQuiz(quiz, self)

    # Finish a quiz  
    def finishQuiz(self, quizId):
        apiComponent = "quiz/users/" + str(self._userId) + "/tests/" + str(quizId) + "/finish"
        self.getJson(apiComponent)    
    
    # Get all skills
    # Return - a list of skills
    def getSkillList(self):
        return self.getJson("skills")
    
    # Get topics of one skill
    def getTopics(self, skillId):
        return self.getJson("skills/" + str(skillId) + "/topics")

    # Get one skill
    def getSkill(self, skillId):
        return self.getJson("skills/" + str(skillId))
    
    # Helper function to send http get and return json
    def getJson(self, apiComponent):
        endpoint = MySwots.API_ENTRY + apiComponent
        r = requests.get(endpoint)
        return r.json()

    # Helper function to send http post and return json
    def postJson(self, apiComponent, postData):
        endpoint = MySwots.API_ENTRY + apiComponent
        r = requests.post(endpoint, json = postData)
        return r.json()


# Unit test
if __name__ == "__main__":
    mySwots = MySwots(19484) # create MySwots instance
    
    '''skills = mySwots.getSkillList()
    print("Skills: ",skills)

    print("================")
    topics = mySwots.getTopics(55)
    print("Topics for skill 55: ", topics)'''

    print("================")
    quiz = mySwots.createQuiz(55, 5, [2125, 2127, 2129, 2131], 10) # Create Quiz
    #quiz = mySwots.loadQuiz(111300)
    print("New created quiz: ", quiz.testId)
    print("Quiz user id: ", quiz.userId)
    print("Quiz questions: ", quiz.questionIds)
    for qId in quiz.questionIds:
        q = quiz.loadQuestion(qId) # Load question
        print("Question: ", q.question)
        for o in q.options: # Question options
            print("  ", o)
        print("Answer: ", q.answer) # Question answer
