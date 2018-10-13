'''
Python SDK for myswots.com api
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
        pass
    
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
    
    def getJson(self, apiComponent):
        endpoint = MySwots.API_ENTRY + apiComponent
        r = requests.get(endpoint)
        return r.json()

    def postJson(self, apiComponent, postData):
        endpoint = MySwots.API_ENTRY + apiComponent
        r = requests.post(endpoint, json = postData)
        return r.json()


if __name__ == "__main__":
    mySwots = MySwots(19484)
    
    '''skills = mySwots.getSkillList()
    print("Skills: ",skills)

    print("================")
    topics = mySwots.getTopics(55)
    print("Topics for skill 55: ", topics)'''

    print("================")
    quiz = mySwots.createQuiz(55, 5, [2125, 2127, 2129, 2131], 10)
    print("New created quiz: ", quiz.testId)
    print("Quiz user id: ", quiz.userId)
    print("Quiz questions: ", quiz.questionIds)
    for qId in quiz.questionIds:
        q = quiz.loadQuestion(qId)
        print("Question: ", q.question)
        for o in q.options:
            print("  ", o)
        print("Answer: ", q.getAnswer())
