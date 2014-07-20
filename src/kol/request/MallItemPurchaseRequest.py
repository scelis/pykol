import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class MallItemPurchaseRequest(GenericRequest):
    """
    Purchases an item from the specified store. This will fail if the price per item is not given
    correctly or if the quantity is higher than the remaining quantity per day. It will purchase
    as many as possible if the quantity is higher than the number in the store.
    """

    def __init__(self, session, storeId, itemId, price, quantity=1):
        super(MallItemPurchaseRequest, self).__init__(session)
        self.url = session.serverURL + 'mallstore.php'
        self.requestData['pwd'] = session.pwd
        self.requestData['buying'] = '1'
        self.requestData['ajax'] = '1'
        self.requestData['whichitem'] = str(itemId) + str(price).zfill(9)
        self.requestData['whichstore'] = storeId
        self.requestData['quantity'] = quantity

    def parseResponse(self):
        cantAffordItemPattern = PatternManager.getOrCompilePattern('cantAffordItem')
        if cantAffordItemPattern.search(self.responseText):
            raise Error.Error("You can not afford to buy this item.", Error.NOT_ENOUGH_MEAT)

        noItemAtThatPricePattern = PatternManager.getOrCompilePattern('mallNoItemAtThatPrice')
        if noItemAtThatPricePattern.search(self.responseText):
            raise Error.Error("That item is not sold here at that price.", Error.ITEM_NOT_FOUND)

        ignoreListPattern = PatternManager.getOrCompilePattern('cantBuyItemIgnoreList')
        if ignoreListPattern.search(self.responseText):
            raise Error.Error("The owner of that store has balleeted you.", Error.USER_IS_IGNORING)

        mallHitLimitPattern = PatternManager.getOrCompilePattern('mallHitLimit')
        if mallHitLimitPattern.search(self.responseText):
            raise Error.Error("You have hit the limit for this item at this store.", Error.LIMIT_REACHED)

        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(items) == 0:
            raise Error.Error("Unknown error: %s" % self.responseText, Error.REQUEST_GENERIC)
        self.responseData["items"] = items

        spentMeatPattern = PatternManager.getOrCompilePattern('meatSpent')
        match = spentMeatPattern.search(self.responseText)
        self.responseData['meatSpent'] = int(match.group(1).replace(',', ''))
