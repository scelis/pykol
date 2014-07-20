import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class TravelingTraderRequest(GenericRequest):
    def __init__(self, session, itemId, quantity=1, tradeAll=False):
        super(TravelingTraderRequest, self).__init__(session)
        self.url = session.serverURL + "traveler.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = "For Gnomeregan!"
        self.requestData['whichitem'] = itemId
        if tradeAll:
            self.requestData['tradeall'] = 1

    def parseResponse(self):
        # Look for known errors. We override the NOT_ENOUGH_MEAT error here because it basically matches the error condition
        # of not having enough currency to buy the particular product. It is not worth creating a one-off error for this
        # particular situation, especially since the trader doesn't deal in meat.
        p = PatternManager.getOrCompilePattern('traderNotTradingForThatItem')
        if p.search(self.responseText):
            raise Error.Error("The trader isn't trading for that item.", Error.ITEM_NOT_FOUND)
        p = PatternManager.getOrCompilePattern('traderCantTradeForThatMany')
        if p.search(self.responseText):
            raise Error.Error("You are unable to trade for that many items.", Error.NOT_ENOUGH_MEAT)
        p = PatternManager.getOrCompilePattern('traderNotEnoughWads')
        if p.search(self.responseText):
            raise Error.Error("You are unable to trade for that many items.", Error.NOT_ENOUGH_MEAT)
        
        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(items) == 0:
            raise Error.Error("Unknown error. No items received.", Error.REQUEST_FATAL)
        self.responseData["items"] = items
