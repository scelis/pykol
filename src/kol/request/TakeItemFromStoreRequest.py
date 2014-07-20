import kol.Error as Error
from kol.util import Report
from kol.manager import PatternManager
from GenericRequest import GenericRequest

class TakeItemFromStoreRequest(GenericRequest):
    """
    Take a single item from your store using the new Mall interface from Sep 2013
    
    Class expects at least an itemId. If no quantity is given, a quantity of 1 is assumed
    
    Todo: add option to remove all of an item. This will require calling StoreInventoryRequest
    and figuring out how many of the item there are.
    """
    
    def __init__(self, session, item):
        super(TakeItemFromStoreRequest, self).__init__(session)
        self.url = session.serverURL + 'backoffice.php'
        self.requestData['action'] = 'removeitem'
        self.requestData['pwd'] = session.pwd
        
        self.requestData['itemid'] = item['itemId']
        if 'quantity' in item:
            self.requestData['qty'] = item['quantity']
        else:
            self.requestData['qty'] = 1
        
    def parseResponse(self):
        # First parse for errors
        notEnoughPattern = PatternManager.getOrCompilePattern("dontHaveThatManyInStore")
        if notEnoughPattern.search(self.responseText):
            raise Error.Error("You either don't have that item, or not enough", Error.ITEM_NOT_FOUND)
            
        # Check if responseText matches the success pattern. If not, raise error.
        itemTakenSuccessfully = PatternManager.getOrCompilePattern("itemTakenSuccessfully")
        if itemTakenSuccessfully.search(self.responseText):
             Report.trace('request', 'Item appears to have been taken')
        else:
            raise Error.Error("Something went wrong with the taking of the item.", Error.ITEM_NOT_FOUND)

