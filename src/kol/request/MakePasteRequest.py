from GenericRequest import GenericRequest
from kol.Error import NotEnoughMeatError, RequestError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class MakePasteRequest(GenericRequest):
    "Creates meat paste, meat stacks, or dense meat stacks."
    
    def __init__(self, session, itemId, quantity=1):
        super(MakePasteRequest, self).__init__(session)
        self.url = session.serverURL + "craft.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'makepaste'
        self.requestData['qty'] = quantity
        
    def parseResponse(self):
        # Check for errors.
        noMeatForPastePattern = PatternManager.getOrCompilePattern('noMeatForMeatpasting')
        if noMeatForPastePattern.search(self.responseText):
            raise NotEnoughMeatError("Unable to make the requested item. You don't have enough meat")
        
        # Get the item(s) we received.
        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(items) > 0:
            self.responseData["items"] = item
        else:
            raise RequestError("Unknown error. No items received.")
