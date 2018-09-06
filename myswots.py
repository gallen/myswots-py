'''
Python SDK for myswots.com api
'''

import requests


# myswots sdk main class.
class MySwots:
    API_ENTRY = "https://myswots.com/api/"
    # Constructor
    def __init__(self, userId):
        self._userId = userId

    # Create test    
    def createQuiz(self, skillId, noOfQuestions, topics):
        pass
        
    # Load existing Quiz with quiz ID
    def loadQuiz(self, quizId):
        pass
    
    # Get all skills
    # Return - a list of skills
    def getSkillList(self):
        return self._getJson("skills")
    
    # Get topics of one skill
    def getTopics(self, skillId):
        return self._getJson("skills/" + str(skillId) + "/topics")

    # Get one skill
    def getSkill(self, skillId):
        return self._getJson("skills/" + str(skillId))
    
    def _getJson(self, apiComponent):
        endpoint = MySwots.API_ENTRY + apiComponent
        r = requests.get(endpoint)
        return r.json()


if __name__ == "__main__":
    mySwots = MySwots(19484)
    skills = mySwots.getSkillList()
    print("Skills: ",skills)

    print("================")
    topics = mySwots.getTopics(55)
    print("Topics for skill 55: ", topics)


    #Quiz = mySwots.createQuiz(55, 5, [2125, 2127, 2129, 2131])
