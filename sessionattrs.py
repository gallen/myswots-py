# Alexa session attributes for myswots

class SessionAttrs:
    # Constructor
    # Construct from either quiz or attrs, but not both
    def __init__(self, quiz=None, attrs=None):
        if quiz != None:
            self._initWithQuiz(quiz)
        elif attrs != None:
            self._initWithAttrs(attrs)
        else:
            raise RuntimeError("Sessaion attribute initialize failed.")
    
    def _initWithQuiz(self, quiz):
        self._attrs = {}
        self._attrs["userId"] = quiz.userId # user Id
        self._attrs["testId"] = quiz.testId # quiz id
        self._attrs["questions"] = quiz.questionIds # question id list
        self._attrs["cur"] = 0 # current question index
        self._attrs["correct"] = 0 # correct statistics
        self._attrs["answer"] = 0
        self._attrs["answerText"] = ""
    
    def _initWithAttrs(self, attrs):
        self._attrs = attrs

    @property
    def attrs(self):
        return self._attrs

    def next(self):
        self._attrs["cur"] += 1

    @property
    def cur(self):
        return self._attrs["questions"][self._attrs['cur']]

    def isLast(self):
        return self._attrs["cur"] >= len(self.attrs['questions']) - 1
    
    def correct(self):
        self._attrs["correct"] += 1

    def wrong(self):
        self._attrs["wrong"]  += 1