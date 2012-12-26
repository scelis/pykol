from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.database import ItemDatabase
import kol.Error as Error

class NashCrosbysStillRequest(GenericRequest):
    def __init__(self, session, itemId, qty):
        super(NashCrosbysStillRequest, self).__init__(session)
        self.url = session.serverURL + "guild.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "stillbooze"
        self.requestData["whichitem"] = itemId
        self.requestData["quantity"] = qty

    def parseResponse(self):
        wrongProfessionPattern = PatternManager.getOrCompilePattern('wrongStillProfession')
        invalidItemPattern = PatternManager.getOrCompilePattern('invalidStillItem')
        ItemNotFoundPattern = PatternManager.getOrCompilePattern('stillItemNotFound')
        maxLimitPattern = PatternManager.getOrCompilePattern('stillMaxLimit')

        if wrongProfessionPattern.search(self.responseText):
            raise Error.Error("You aren't a Disco Bandit or Accordion Thief.", Error.USER_IS_WRONG_PROFESSION)
        if invalidItemPattern.search(self.responseText):
            raise Error.Error("You can\'t improve that item.", Error.INVALID_ITEM)
        if ItemNotFoundPattern.search(self.responseText):
            raise Error.Error("Not enough of that item.", Error.ITEM_NOT_FOUND)
        if maxLimitPattern.search(self.responseText):
            raise Error.Error("Still can\'t be used anymore today.", Error.LIMIT_REACHED)

        # Find the items attached to the message.
        singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
        match = singleItemPattern.search(self.responseText)
        if match:
            descId = int(match.group(1))
            item = ItemDatabase.getOrDiscoverItemFromDescId(descId, self.session)
            item["quantity"] = 1
        else:
            multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
            match = multiItemPattern.search(self.responseText)
            if match:
                descId = int(match.group(1))
                item = ItemDatabase.getOrDiscoverItemFromDescId(descId, self.session)
                quantity = int(match.group(2).replace(',', ''))
                item["quantity"] = quantity
            else:
                raise Error.Error("Unknown error.", Error.REQUEST_GENERIC)

        self.responseData["item"] = item
