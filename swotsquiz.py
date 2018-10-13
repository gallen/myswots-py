'''
Python SDK for myswots.com api
'''
import swotsquestion

# Swots quiz class.
# User should not create object of this class directly. 
# Object of this class should be created by MySwots.createQuiz or MySwots.loadQuiz
class SwotsQuiz:
    # Constructor
    def __init__(self, quizDict, swots):
        self._quiz = quizDict
        self._swots = swots
    
    @property
    def userId(self):
        return self._swots.userId

    @property
    def testId(self):
        return self._quiz["testId"]

    @property
    def questionIds(self):
        return [q["questionId"] for q in self._quiz["questionsMetadata"]]

    # Load one question
    def loadQuestion(self, questionId):
        qDict = self._swots.getJson("quiz/users/" + str(self.userId) 
            + "/tests/" + str(self.testId)
            + "/question/" + str(questionId))
        return swotsquestion.SwotsQuestion(self, questionId, qDict)

    # Load answer for one question
    def loadAnswer(self, questionId):
        pass
    
    # Get status for one question
    def getQuestionStatus(self, questionId):
        pass

    # Finish this test
    def finish(self):
        pass

    # Get result for this test
    def getResult(self):
        pass
    
