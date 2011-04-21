import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager

class PulverizeRequest(GenericRequest):
    def __init__(self, session, itemId, itemQuantity=1):
        super(PulverizeRequest, self).__init__(session)
        self.url = session.serverURL + "craft.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "pulverize"
        self.requestData["mode"] = "smith"
        self.requestData["smashitem"] = itemId
        self.requestData["qty"] = itemQuantity
        self.itemId = itemId
        self.quantity = itemQuantity

    def parseResponse(self):
        cantPulverizePattern = PatternManager.getOrCompilePattern('cantPulverizeItem')
        if cantPulverizePattern.search(self.responseText) != None:
            item = ItemDatabase.getOrDiscoverItemFromId(self.itemId, self.session)
            raise Error.Error("'%s' is not an item that can be pulverized." % item["name"], Error.WRONG_KIND_OF_ITEM)

        notEnoughItemsPattern = PatternManager.getOrCompilePattern('notEnoughItems')
        if notEnoughItemsPattern.search(self.responseText) != None:
            item = ItemDatabase.getOrDiscoverItemFromId(self.itemId, self.session)
            if self.quantity == 1:
                itemStr = item["name"]
            else:
                itemStr = item["plural"]
            raise Error.Error("You do not have %s (%s)." % (itemStr, self.quantity), Error.ITEM_NOT_FOUND)

        items = []

        singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
        for match in singleItemPattern.finditer(self.responseText):
            descId = int(match.group(1))
            item = ItemDatabase.getOrDiscoverItemFromDescId(descId, self.session)
            item["quantity"] = 1
            items.append(item)

        multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
        for match in multiItemPattern.finditer(self.responseText):
            descId = int(match.group(1))
            quantity = int(match.group(2).replace(',', ''))
            item = ItemDatabase.getOrDiscoverItemFromDescId(descId, self.session)
            item["quantity"] = quantity
            items.append(item)

        self.responseData["results"] = items
