import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class MeatpastingRequest(GenericRequest):

    def __init__(self, session, itemid1, itemid2, numPasted=1, makeMax=False):
        super(MeatpastingRequest, self).__init__(session)
        self.url = session.serverURL + "craft.php"
        self.requestData['mode'] = 'combine'
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'craft'
        self.requestData['qty'] = numPasted
        self.requestData['a'] = itemid1
        self.requestData['b'] = itemid2
        if makeMax:
            self.requestData['max'] = "on"

    def parseResponse(self):
        # Check for errors.
        dontHaveMeatpastePattern = PatternManager.getOrCompilePattern('noMeatpaste')
        itemsDontMeatpastePattern = PatternManager.getOrCompilePattern('itemsDontMeatpaste')
        dontHaveItemsPattern = PatternManager.getOrCompilePattern('dontHaveItemsMeatpaste')
        if dontHaveMeatpastePattern.search(self.responseText):
            e = Error.Error("Unable to combine items. You don't have any meatpaste.", Error.ITEM_NOT_FOUND)
            e.itemId = 25
            raise e
        elif itemsDontMeatpastePattern.search(self.responseText):
            raise Error.Error("Unable to combine items. The submitted ingredients do not meatpaste together.", Error.RECIPE_NOT_FOUND)
        elif dontHaveItemsPattern.search(self.responseText):
            raise Error.Error("Unable to combine items. You don't have all of the items you are trying to meatpaste.", Error.ITEM_NOT_FOUND)

        # Find the items attached to the message.
        items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(items) > 0:
            self.responseData["items"] = items
        else:
            raise Error.Error("Unknown error meatpasting items: %s" % self.responseText, Error.REQUEST_FATAL)
