import kol.Error as Error
from kol.util import Report
from kol.manager import PatternManager
from GenericRequest import GenericRequest

import time

class PutItemInStoreRequest(GenericRequest):
    """
    Add a single item to your store. The interface to the mall was updated on Sept 13, 2013.
    It looks like items are now added only one at a time.
    
    Notes about new URL: http://www.kingdomofloathing.com/backoffice.php
    itemid: this will contain an "h" in front of it if the item is in Hangk's
    
    There is now a submitted field name '_'. This appears to be the milliseconds since epoch.
    Testing will need to be done to see how important this is. Presumably you could just append
    000 after the current seconds since epoch.
    """
    
    def __init__(self, session, item):
        super(PutItemInStoreRequest, self).__init__(session)
        self.url = session.serverURL + 'backoffice.php'
        self.requestData['action'] = "additem"
        self.requestData['pwd'] = session.pwd
        self.requestData['_'] = int(time.time() * 1000)
        self.requestData['ajax'] = 1

        
        if "isInHangks" in item:
            self.requestData['itemid'] = "h%s" % item["id"]
        else:
            self.requestData['itemid'] = item["id"]
        if "price" in item:
            self.requestData['price'] = item["price"]
        else:
            self.requestData['price'] = "999999999"
        if "limit" in item:
            self.requestData['limit'] = item["limit"]
        else:
            self.requestData['limit'] = ""
        if "quantity" in item:
            self.requestData['quantity'] = item["quantity"]
        else:
            self.requestData['quantity'] = "1"

    def parseResponse(self):
        # First parse for errors
        notEnoughPattern = PatternManager.getOrCompilePattern("dontHaveEnoughOfItem")
        if notEnoughPattern.search(self.responseText):
            raise Error.Error("You don't have that many of that item.", Error.ITEM_NOT_FOUND)
        
        dontHaveItemPattern = PatternManager.getOrCompilePattern("dontHaveThatItem")
        if dontHaveItemPattern.search(self.responseText):
            raise Error.Error("You don't have that item.", Error.ITEM_NOT_FOUND)
            
        # Check if responseText matches the success pattern. If not, raise error.
        itemAddedSuccessfully = PatternManager.getOrCompilePattern("itemAddedSuccessfully")
        if itemAddedSuccessfully.search(self.responseText):
             Report.trace('request', 'Item appears to have been added')
        else:
            raise Error.Error("Something went wrong with the adding.", Error.ITEM_NOT_FOUND)
        