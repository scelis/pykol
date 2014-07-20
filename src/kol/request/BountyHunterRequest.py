from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class BountyHunterRequest(GenericRequest):
    """Interacts with the Bounty Hunter Hunter in the Forest Village."""
    
    VISIT = None
    ACCEPT_BOUNTY = 'takebounty'
    ABANDON_BOUNTY = 'abandonbounty'
    BUY = 'buy'
    
    def __init__(self, session, action=None, item=None, quantity=None):
        """Initialize a Bounty Hunter Hunter request.
        
        Args:
            session: A valid logged in session.
            action: Optional action. If None, the request just "visits" the Bounty Hunter Hunter and 
                determines which bounties are available.
                Otherwise, one of: 'takebounty', 'abandonbounty' or 'buy'
            item: Optional item id. When accepting bounty assignment, this is the id of the bounty item
                (for example, 2099 for hobo gristle). 
                When buying items using filthy lucre, this is the descid of the purchased item 
                (e.g. 810074020 for Manual of Transcendent Olfaction).
            quantity: Optional number of items being purchased for filthy lucre.
        """
        super(BountyHunterRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "bhh.php"
        
        self.requestData["pwd"] = session.pwd
        
        if action:
            self.requestData['action'] = action
        if quantity:
            self.requestData['quantity'] = quantity
        if item:
            self.requestData['whichitem'] = item

    def parseResponse(self):
        response = {}
        
        bountyAvailablePattern = PatternManager.getOrCompilePattern('bountyAvailable')
        if bountyAvailablePattern.search(self.responseText):
            bountyAvailable = True
        else:
            bountyAvailable = False

        bountyChosenPattern = PatternManager.getOrCompilePattern('bountyChosen')
        bountyActivePattern1 = PatternManager.getOrCompilePattern('bountyActive1')
        bountyActivePattern2 = PatternManager.getOrCompilePattern('bountyActive2')
        
        if bountyChosenPattern.search(self.responseText) or \
            bountyActivePattern1.search(self.responseText) or \
            bountyActivePattern2.search(self.responseText):
                bountyActive = True
        else:
            bountyActive = False

        dailyBounties = []
        if bountyAvailable:
            bountyPattern = PatternManager.getOrCompilePattern('dailyBountyItem')
            for match in bountyPattern.finditer(self.responseText):
                itemId = int(match.group('itemid'))
                item = ItemDatabase.getItemFromId(itemId)
                dailyBounties.append(item)
        
        response['bountyAvailable'] = bountyAvailable
        response['bountyActive'] = bountyActive
        response['dailyBounties'] = dailyBounties
        
        self.responseData = response
