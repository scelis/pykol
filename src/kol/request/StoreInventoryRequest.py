import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import StringUtils

class StoreInventoryRequest(GenericRequest):
    "This class is used to get a list of items currently in a user's store"

    def __init__(self, session):
            super(StoreInventoryRequest, self).__init__(session)
            self.url = session.serverURL + 'backoffice.php?which=1'

    def parseResponse(self):
        """
        Searches backoffice.php for item name, quantity, price, limit, and ID.
        Returns the items with the usual keys in the item data base along with:

            quantity -- The number of the item in your mall store.
               price -- The price of the item in your mall store.
               limit -- The limit on the item in your mall store.
            cheapest -- The cheapest in mall. This includes limited items, use at own risk.
             orderId -- Item order in your store. 0 is the first listed and so on.
             
        RegExp match notes: Group 3,6,9, and 11 are garbage HTML data.
        """
        storeInventoryPattern = PatternManager.getOrCompilePattern('storeInventory')

        items = []
        for match in storeInventoryPattern.finditer(self.responseText):
            descId = match.group(1)
            orderId = match.group(2)
            name = match.group(4)
            quantity = match.group(5)
            itemID = int(match.group(7))
            item = ItemDatabase.getOrDiscoverItemFromId(itemID, self.session)
            price = match.group(8)
            limit = int(match.group(10))
            cheapest = int(match.group(12))
            
            item["orderId"] = orderId
            item["quantity"] = quantity
            item["price"] = price
            item["limit"] = limit
            item["cheapest"] = cheapest
            items.append(item)

        self.responseData["items"] = items