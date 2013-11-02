import kol.Error as Error
from kol.util import Report
from kol.manager import PatternManager
from GenericRequest import GenericRequest

import time

class UpdateItemInStoreRequest(GenericRequest):
    """
    Update the limit and price of items in your store.
    
    This expects an itemId, a limit and a price for each item.
    """
    
    def __init__(self, session, items):
        super(UpdateItemInStoreRequest, self).__init__(session)
        self.url = session.serverURL + 'backoffice.php'
        self.requestData['action'] = "updateinv"
        self.requestData['pwd'] = session.pwd
        self.requestData["ajax"] = 1
        self.requestData['_'] = int(time.time() * 1000)
        
        for item in items:
            priceString = "price[%s]" % (item["itemId"])
            self.requestData[priceString] = item["price"]

            limitString = "limit[%s]" % (item["itemId"])
            self.requestData[limitString] = item["limit"]
            
    def parseResponse(self):
        # Parse to see if nothing was updated
        priceNotUpdatedPattern = PatternManager.getOrCompilePattern("mallPriceNotUpdated")
        if priceNotUpdatedPattern.search(self.responseText):
            self.responseData["priceUpdated"] = False
        else:
            self.responseData["priceUpdated"] = True
        