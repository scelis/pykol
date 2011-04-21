from ApiRequest import ApiRequest
from kol.database import ItemDatabase

class InventoryRequest(ApiRequest):
    "This class is used to get a list of items in the user's inventory."

    def __init__(self, session, which=None):
        super(InventoryRequest, self).__init__(session)
        self.requestData["what"] = "inventory"
        self.ignoreItemDatabase = False

    def parseResponse(self):
        super(InventoryRequest, self).parseResponse()

        items = []
        for itemId, quantity in self.jsonData.iteritems():
            if self.ignoreItemDatabase:
                item = {}
                item["id"] = int(itemId)
                item["quantity"] = int(quantity)
                items.append(item)
            else:
                item = ItemDatabase.getOrDiscoverItemFromId(int(itemId), self.session)
                item["quantity"] = int(quantity)
            items.append(item)

        self.responseData["items"] = items
