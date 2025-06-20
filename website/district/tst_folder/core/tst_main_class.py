from django.test import TransactionTestCase


class MainClassTest(TransactionTestCase):

    @staticmethod
    def getSortedTestCaseNames():
        return []

    def __init__(self, methodName=''):
        super().__init__(methodName)



