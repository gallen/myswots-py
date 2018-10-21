'''
Python SDK for myswots.com api
'''

from bs4 import BeautifulSoup

def remove_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.text

# Swots question
# User should not create object of this class directly.
# # Object of this class should be created by SwotsQuiz.loadQuestion
class SwotsQuestion:
    def __init__(self, quiz, questionId, qDict):
        self._quiz = quiz
        self._qDict = qDict
        self._questionId = questionId
        self._answer = None

    # Question text
    @property
    def question(self):
        return remove_tags(self._qDict["questionText"])

    # Question ID
    @property
    def questionId(self):
        return self._questionId

    # Question options (selections)
    @property
    def options(self):
        return self._qDict["options"]

    # Answer
    @property
    def answer(self):
        if self._answer == None:
            self._answer = self._getAnswer()
        return self._answer


    def _getAnswer(self, myAnswer=1, timeSpent=5):
        ret = self.swots.postJson("/quiz/users/" + str(self._quiz.userId)
            + "/tests/" + str(self._quiz.testId)
            + "/feedback/" + str(self.questionId), {"anser": myAnswer, "timeSpent": timeSpent})
        return ret["answer"]

    # Helper property to get MySwots instance
    @property
    def swots(self):
        return self._quiz._swots
        
