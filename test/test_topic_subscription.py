# pylint: disable=C0325,C0103,C1801
import os
import errno
import time
import unittest
import json

test_dir = os.path.dirname(os.path.abspath(__file__))

class TestTopicSubscriptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setting up suite: {}".format(cls))

    @classmethod
    def tearDownClass(cls):
        print("tearing down suite: {}".format(cls))

    def setUp(self):
        test_name = self.id().split('.')[-1]

    def tearDown(self):
        print("stopping test: {}".format(self.id().split('.')[-1]))

    def test_easy_case(self):
        self.assertTrue(True)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
