'''
Python SDK for myswots.com api
'''

from bs4 import BeautifulSoup

def remove_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.text

# Swots question
class SwotsQuestion:
    def __init__(self, quiz, questionId, qDict):
        self._quiz = quiz
        self._qDict = qDict
        self._questionId = questionId

    @property
    def question(self):
        return remove_tags(self._qDict["questionText"])

    @property
    def questionId(self):
        return self._questionId

    @property
    def options(self):
        return self._qDict["options"]
    
    @property
    def swots(self):
        return self._quiz._swots

    def getAnswer(self, myAnswer=1, timeSpent=5):
        ret = self.swots.postJson("/quiz/users/" + str(self._quiz.userId)
            + "/tests/" + str(self._quiz.testId)
            + "/feedback/" + str(self.questionId), {"anser": myAnswer, "timeSpent": timeSpent})
        return ret["answer"]
        
