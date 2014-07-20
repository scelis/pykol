import TestData
from kol.Session import Session

import unittest

class Main(unittest.TestCase):
    def runTest(self):
        s = Session()
        s.login(TestData.data["userName"], TestData.data["password"])
        self.assert_(s.isConnected == True)
        TestData.data["session"] = s
