from ApiRequest import ApiRequest
from kol.database import ItemDatabase

class ItemInformationRequest(ApiRequest):
    "This class is used to get information about a particular item."

    def __init__(self, session, itemId):
        super(ItemInformationRequest, self).__init__(session)
        self.requestData["what"] = "item"
        self.requestData["id"] = itemId
        self.itemId = itemId

    def parseResponse(self):
        super(ItemInformationRequest, self).parseResponse()
        
        item = {}
        data = self.jsonData
        item["id"] = self.itemId
        item["descId"] = int(data["descid"])
        item["name"] = data["name"]
        if "plural" in data and len(data["plural"]) > 0:
            item["plural"] = data["plural"]
        if "picture" in data and len(data["picture"]) > 0:
            item["image"] = "%s.gif" % data["picture"]
        if "type" in data:
            item["type"] = data["type"]
            if item["type"] == "gift":
                item["type"] = "gift package"
        if "sellvalue" in data and int(data["sellvalue"] > 0):
            item["autosell"] = int(data["sellvalue"])
        if "power" in data:
            item["power"] = int(data["power"])
        if "hands" in data and int(data["hands"] > 0):
            item["numHands"] = int(data["hands"])
        if "cantransfer" in data and data["cantransfer"] == "1":
            item["canTransfer"] = True
        if "cook" in data and data["cook"] == "1":
            item["isCookingIngredient"] = True
        if "cocktail" in data and data["cocktail"] == "1":
            item["isCocktailcraftingIngredient"] = True
        if "jewelry" in data and data["jewelry"] == "1":
            item["isJewelrymakingComponent"] = True
        if "smith" in data and data["smith"] == "1":
            item["isMeatsmithingComponent"] = True
        if "combine" in data and data["combine"] == "1":
            item["isMeatpastingComponent"] = True
        if "fancy" in data and data["fancy"] == "1":
            item["isFancy"] = True
        if "quest" in data and data["quest"] == "1":
            item["isQuestItem"] = True
        if "candiscard" in data and data["candiscard"] == "1":
            item["isDiscardable"] = True
        if "unhardcore" in data and data["unhardcore"] == "1":
            item["isHardcoreDenied"] = True
        self.responseData["item"] = item
