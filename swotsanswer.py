from utils import remove_tags

class SwotsAnswer:
    def __init__(self, swots, testId, questionId, answer, timeSpent):
        feedback = swots.postJson("/quiz/users/" + str(swots.userId)
                + "/tests/" + str(testId)
                + "/feedback/" + str(questionId), {"answer": answer, "timeSpent": timeSpent})
        self.answer = feedback["answer"]
        self.solution = remove_tags(feedback["solution"]["solutionText"]).strip()
        self.answerText = remove_tags(feedback["options"][self.answer - 1])
        self.status = feedback["userStats"]["status"]

