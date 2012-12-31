import TestData
from kol.request.BountyHunterRequest import BountyHunterRequest
import unittest

class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        bountyRequest = BountyHunterRequest(s)
        
        response = bountyRequest.doRequest()
        
        if response['bountyAvailable']:
            self.assertFalse(response['bountyActive'], "bountyActive should not be true when a bounty is available")
            
            bounties = response['dailyBounties']
            
            self.assertEquals(len(bounties), 3, 'Bounty Hunter Hunter should have 3 daily bounties available')
            for bountyItem in bounties:
                self.assertTrue(bountyItem['isBounty'])

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