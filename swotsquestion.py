'''
Python SDK for myswots.com api
'''


from utils import remove_tags

# Swots question
# User should not create object of this class directly.
# # Object of this class should be created by SwotsQuiz.loadQuestion
class SwotsQuestion:
    def __init__(self, quiz, questionId, qDict):
        self._quiz = quiz
        self._qDict = qDict
        self._questionId = questionId
        self._answer = None
        self._feedback = None

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
        return [remove_tags(qo) for qo in self._qDict["options"]]

    # Answer
    @property
    def answer(self):
        self._getFeedback()
        return self._feedback["answer"]

    @property
    def solution(self):
        self._getFeedback()
        return remove_tags(self._feedback["solution"]["solutionText"])
    
    def _getFeedback(self, myAnswer = 1, timeSpent = 5):
        if self._feedback == None:
            self._feedback = self.swots.postJson("/quiz/users/" + str(self._quiz.userId)
                + "/tests/" + str(self._quiz.testId)
                + "/feedback/" + str(self.questionId), {"answer": myAnswer, "timeSpent": timeSpent})     

    # Helper property to get MySwots instance
    @property
    def swots(self):
        return self._quiz._swots
        
