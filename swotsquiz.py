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
    
    # userId
    @property
    def userId(self):
        return self._swots.userId

    # testId (quizId)
    @property
    def testId(self):
        return self._quiz["testId"]

    # questionId list
    @property
    def questionIds(self):
        return [q["questionId"] for q in self._quiz["questionsMetadata"]]

    # Load one question
    def loadQuestion(self, questionId):
        qDict = self._swots.getJson("quiz/users/" + str(self.userId) 
            + "/tests/" + str(self.testId)
            + "/question/" + str(questionId))
        return swotsquestion.SwotsQuestion(self, questionId, qDict)

    # Get status for one question
    def getQuestionStatus(self, questionId):
        pass


    # Get result for this test
    def getResult(self):
        pass
    
