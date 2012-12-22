import TestData
import TestGetItemDescriptionRequest
import TestItemDatabase
import TestBountyHunter
import TestLogin
import TestLogout
from kol.util import Report

import sys
import unittest

def main(argv=sys.argv):
    TestData.data["userName"] = argv[1]
    TestData.data["password"] = argv[2]
    Report.activeSections = []
    
    # Add the tests.
    suite = unittest.TestSuite()
    suite.addTest(TestItemDatabase.Main())
    suite.addTest(TestLogin.Main())
    suite.addTest(TestGetItemDescriptionRequest.Main())
    suite.addTest(TestBountyHunter.Main())
    suite.addTest(TestLogout.Main())
    
    # Run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
