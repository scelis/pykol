import kol.Error as Error
from kol.util import Report
from kol.manager import PatternManager
from kol.database import ItemDatabase
from GenericRequest import GenericRequest

class SearchMallPriceRequest(GenericRequest):
    """
    Search the mall for the lowest prices of an item. This will return the
    4 lowest unlimited prices, and if applicable, the 3 lowest limited 
    prices with their limit amount per day.
    
    Unlimited and Limited patterns had to be broken apart, since not all items
    have a limited quantity. 
    
    I'm not sure what the counts when doing a search are, but I'm including it anyways.
    """
    
    def __init__(self, session, itemId):
    
        super(SearchMallPriceRequest, self).__init__(session)
        self.url = session.serverURL + 'backoffice.php'
        self.requestData['action'] = "prices"
        self.requestData['pwd'] = session.pwd
        self.requestData['iid'] = itemId
        
        self.itemId = itemId
        
    def parseResponse(self):
        item = ItemDatabase.getOrDiscoverItemFromId(int(self.itemId), self.session)
        mallPricesUnlimitedPattern = PatternManager.getOrCompilePattern('mallPricesUnlimited')

        for match in mallPricesUnlimitedPattern.finditer(self.responseText):
            unlimited = []
            price = {"price" : match.group(1), "count" : match.group(2)}
            unlimited.append(price)
            price = {"price" : match.group(3), "count" : match.group(4)}
            unlimited.append(price)       
            price = {"price" : match.group(5), "count" : match.group(6)}
            unlimited.append(price)        
            price = {"price" : match.group(7), "count" : match.group(8)}
            unlimited.append(price)             
            
            item["unlimited"] = unlimited

        mallPricesLimitedPattern = PatternManager.getOrCompilePattern('mallPricesLimited')

        for match in mallPricesLimitedPattern.finditer(self.responseText):            
            limited = []
            price = {"price" : match.group(9), "limit" : match.group(10), "count" : match.group(11)}
            limited.append(price)
            price = {"price" : match.group(12), "limit" : match.group(13), "count" : match.group(14)}
            limited.append(price)
            price = {"price" : match.group(15), "limit" : match.group(16), "count" : match.group(17)}
            limited.append(price)
            
            item["limited"] = limited

        self.responseData["item"] = item