import kol.Error as Error
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class CookingRequest(GenericRequest):

    def __init__(self, session, itemid1, itemid2, numMake=1, makeMax=False):
        super(CookingRequest, self).__init__(session)
        self.url = session.serverURL + "craft.php"
        self.requestData['mode'] = 'cook'
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'craft'
        self.requestData['qty'] = numMake
        self.requestData['a'] = itemid1
        self.requestData['b'] = itemid2

        if makeMax:
            self.requestData['max'] = "on"

    def parseResponse(self):
        itemsDontMakeFoodPattern = PatternManager.getOrCompilePattern('itemsDontCook')
        dontHaveSkillPattern = PatternManager.getOrCompilePattern('dontHaveSkillToCook')
        dontHaveItemsPattern = PatternManager.getOrCompilePattern('dontHaveItemsForCook')
        dontHaveAdventuresPattern = PatternManager.getOrCompilePattern('dontHaveAdventuresToCook')
        chefExplosionPattern = PatternManager.getOrCompilePattern('chefExplosion')
        # Check for errors.
        if itemsDontMakeFoodPattern.search(self.responseText):
            raise Error.Error("Unable to make food. The submitted ingredients do not cook together.", Error.RECIPE_NOT_FOUND)
        elif dontHaveSkillPattern.search(self.responseText):
            raise Error.Error("Unable to make food. We are not skilled enough.", Error.SKILL_NOT_FOUND)
        elif dontHaveItemsPattern.search(self.responseText):
            raise Error.Error("Unable to make food. You don't have all of the items you are trying to cook.", Error.ITEM_NOT_FOUND)
        elif dontHaveAdventuresPattern.search(self.responseText):
            raise Error.Error("Unable to cook food(s). We don't have enough adventures.", Error.NOT_ENOUGH_ADVENTURES)

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

        # Check for an explosion
        if chefExplosionPattern.search(self.responseText):
            self.responseData["explosion"] = 1
            #TODO: Remove the items that came from the explosion

        self.responseData["food"] = item
