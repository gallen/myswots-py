'''
Python SDK for myswots.com api
'''

# Swots test class.
# User should not create object of this class directly. 
# Object of this class should be created by MySwots.createTest or MySwots.loadTest
class SwotsTest:
    # Constructor
    def __init__(self):
        pass
    
    # Load one question
    def loadQuestion(self, questionId):
        pass

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
    
