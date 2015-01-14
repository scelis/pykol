import TestData
from kol.request.BountyHunterRequest import BountyHunterRequest
import unittest

# TODO: This test needs to be redone, since the BHH interface has changed
class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        bountyRequest = BountyHunterRequest(s)
        
        response = bountyRequest.doRequest()
        
        if response['bountyAvailable']:
            self.assertFalse(response['bountyActive'], "bountyActive should not be true when a bounty is available")

            # Pick the first bounty and accept it
            bountyId = bounties[0]['id']
            acceptBountyRequest = BountyHunterRequest(s, action=BountyHunterRequest.ACCEPT_BOUNTY, item=bountyId)
            response = acceptBountyRequest.doRequest()
            self.assertTrue(response['bountyActive'], "bountyActive should be set to true after an accept requestio0k-p")
            self.assertFalse(response['bountyAvailable'], "bountyAvailable should be false after accepting the bounty")
             
            # Abandon the bounty
            abandonBountyRequest = BountyHunterRequest(s, action=BountyHunterRequest.ABANDON_BOUNTY)
            response = abandonBountyRequest.doRequest()
            self.assertTrue(response['bountyAvailable'], "bountyAvailable should be true again after abandoning the bounty")