'''
Python SDK for myswots.com api
'''

from bs4 import BeautifulSoup

def remove_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.text

# Swots question
class SwotsQuestion:
    def __init__(self, quiz, qDict):
        self._quiz = quiz
        self._qDict = qDict

    @property
    def question(self):
        return remove_tags(self._qDict["questionText"])

    @property
    def options(self):
        return self._qDict["options"]