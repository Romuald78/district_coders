import os
import unittest

from django.test.runner import DiscoverRunner

from district.tst_folder.core.tst_loader import DistrictTestLoader
from website.settings import BASE_DIR


class DistrictTestRunner(DiscoverRunner):

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        loader = DistrictTestLoader()

        if test_labels:
            suite = unittest.TestSuite()
            for label in test_labels:
                path = os.path.join(BASE_DIR,label.replace(".", "/"))
                if os.path.isdir(path) :
                    suite.addTests(loader.discover(label))
                else :
                    suite.addTests(loader.loadTestsFromName(label))

        else:
            suite = loader.discover(start_dir='district')

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)
        return suite