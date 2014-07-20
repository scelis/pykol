from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager

class MalusRequest(GenericRequest):
    def __init__(self, session, itemId, numTimes):
        super(MalusRequest, self).__init__(session)
        self.url = session.serverURL + "guild.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "malussmash"
        self.requestData["whichitem"] = itemId
        self.requestData["quantity"] = numTimes

    def parseResponse(self):
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
