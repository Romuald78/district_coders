import unittest
from typing import Type, Sequence
from unittest import TestLoader

from district.tst_folder.core.tst_main_class import MainClassTest


class DistrictTestLoader(TestLoader):

    @classmethod
    def getTestCaseNames(cls, testCaseClass: Type[unittest.case.TestCase]) -> Sequence[str]:
        result = []
        # get sorted test cases if possible
        if issubclass(testCaseClass, MainClassTest):
            result = testCaseClass.getSortedTestCaseNames()
        # else get django default test case order
        if len(result) == 0:
            result = super().getTestCaseNames(cls, testCaseClass)
        return result

    # def loadTestsFromModule(self, module, pattern=None):
    #     suite = unittest.TestSuite()
    #
    #     # TODO + modif Runner to be compliant with
    #     suite.addTests(self.loadTestsFromTestCase(__my_class_name__))
    #
    #     return suite