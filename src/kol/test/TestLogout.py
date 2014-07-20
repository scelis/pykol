import TestData

import unittest

class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        s.logout()
        self.assert_(s.isConnected == False)
