import kol.Error as Error
from kol.database import ItemDatabase
from kol.util import ParseResponseUtils
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class HermitRequest(GenericRequest):

    def __init__(self, session, item, quantity=1):
        super(HermitRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "hermit.php"
        self.requestData['action'] = "trade"
        self.requestData['quantity'] = quantity
        self.requestData['whichitem'] = item

    def parseResponse(self):
        notEnoughCloversPattern = PatternManager.getOrCompilePattern('notEnoughClovers')
        noTrinketsPattern = PatternManager.getOrCompilePattern('noTrinkets')
        noHermitPermitPattern = PatternManager.getOrCompilePattern('noHermitPermits')
        notHermitItemPattern = PatternManager.getOrCompilePattern('notHermitItem')

        # Check for errors.
        if notEnoughCloversPattern.search(self.responseText):
            e = Error.Error("The Hermit doesn't have enough clovers for that.", Error.ITEM_NOT_FOUND)
            e.itemId = 24
            raise e
        if noTrinketsPattern.search(self.responseText):
            e = Error.Error("You don't have enough worthless items for that.", Error.ITEM_NOT_FOUND)
            e.itemId = 43
            raise e
        if noHermitPermitPattern.search(self.responseText):
            e = Error.Error("You don't have enough hermit permits for that.", Error.ITEM_NOT_FOUND)
            e.itemId = 42
            raise e
        if notHermitItemPattern.search(self.responseText):
            e = Error.Error("The Hermit doesn't have any of those.", Error.ITEM_NOT_FOUND)
            e.itemId = self.requestData['whichitem']
            raise e

        response = {}
        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(items) > 0:
            response["items"] = items
        self.responseData = response
