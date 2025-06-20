import unittest

from django.test.runner import DiscoverRunner

from district.tst_folder.core.tst_loader import DistrictTestLoader


class DistrictTestRunner(DiscoverRunner):

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        loader = DistrictTestLoader()

        if test_labels:
            suite = unittest.TestSuite()
            for label in test_labels:
                suite.addTests(loader.loadTestsFromName(label))
        else:
            suite = loader.discover(start_dir='district')

        if extra_tests:
            for test in extra_tests:
                suite.addTest(test)
        return suite