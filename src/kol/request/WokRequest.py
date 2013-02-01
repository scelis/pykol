import kol.Error as Error
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class WokRequest(GenericRequest):

    def __init__(self, session, itemid1, numMake=1):
        super(WokRequest, self).__init__(session)
        self.url = session.serverURL + "guild.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'wokcook'
        self.requestData['qty'] = numMake
        self.requestData['whichitem'] = itemid1


    def parseResponse(self):
        noWokAccess = PatternManager.getOrCompilePattern('noWokAccess')
        itemsDontMakeFoodPattern = PatternManager.getOrCompilePattern('dontHaveItemsForWok')
        dontHaveSkillPattern = PatternManager.getOrCompilePattern('dontHaveSkillForWok')
        dontHaveAdventuresPattern = PatternManager.getOrCompilePattern('dontHaveAdventuresForWok')
        # Check for errors.
        if noWokAccess.search(self.responseText):
            raise Error.Error("Unable to use the Wok of Ages. I can't get to the Wok!", Error.RECIPE_NOT_FOUND)
        elif dontHaveSkillPattern.search(self.responseText):
            raise Error.Error("Unable to use the Wok of Ages. I am not skilled enough.", Error.SKILL_NOT_FOUND)
        elif itemsDontMakeFoodPattern.search(self.responseText):
            raise Error.Error("Unable to use the Wok of Ages. Invalid ingredients.", Error.ITEM_NOT_FOUND)
        elif dontHaveAdventuresPattern.search(self.responseText):
            raise Error.Error("Unable to use the Wok of Agles. I don't have enough adventures.", Error.NOT_ENOUGH_ADVENTURES)

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

        self.responseData["wok"] = item
