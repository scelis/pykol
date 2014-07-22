from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ItemDescriptionRequest(GenericRequest):
    "Gets the description of an item and then parses various information from the response."

    def __init__(self, session, descId):
        super(ItemDescriptionRequest, self).__init__(session)
        self.url = session.serverURL + "desc_item.php?whichitem=%s" % descId

    def parseResponse(self):
        # Get the item name.
        itemNamePattern = PatternManager.getOrCompilePattern("itemName")
        match = itemNamePattern.search(self.responseText)
        self.responseData["name"] = match.group(1)

        # Get the item image.
        imagePattern = PatternManager.getOrCompilePattern("itemImage")
        match = imagePattern.search(self.responseText)
        self.responseData["image"] = match.group(1)

        # Get the item type.
        typePattern = PatternManager.getOrCompilePattern("itemType")
        match = typePattern.search(self.responseText)
        if match:
            self.responseData["type"] = match.group(1).rstrip()

        # Get the autosell value.
        autosellPattern = PatternManager.getOrCompilePattern("itemAutosell")
        match = autosellPattern.search(self.responseText)
        if match:
            self.responseData["autosell"] = int(match.group(1))
        else:
            self.responseData["autosell"] = 0

        # See if this is a cooking ingredient.
        cookingPattern = PatternManager.getOrCompilePattern("isCookingIngredient")
        match = cookingPattern.search(self.responseText)
        if match:
            self.responseData["isCookingIngredient"] = True

        # See if the item is a cocktailcrafting ingredient.
        cocktailcraftingPattern = PatternManager.getOrCompilePattern("isCocktailcraftingIngredient")
        match = cocktailcraftingPattern.search(self.responseText)
        if match:
            self.responseData["isCocktailcraftingIngredient"] = True

        # See if the item is a meatsmithing component.
        meatsmithingPattern = PatternManager.getOrCompilePattern("isMeatsmithingComponent")
        match = meatsmithingPattern.search(self.responseText)
        if match:
            self.responseData["isMeatsmithingComponent"] = True

        # See if the item is a jewelrymaking component.
        jewelrymakingPattern = PatternManager.getOrCompilePattern("isJewelrymakingComponent")
        match = jewelrymakingPattern.search(self.responseText)
        if match:
            self.responseData["isJewelrymakingComponent"] = True
