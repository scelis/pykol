import TestData
from kol.database import ItemDatabase
from kol.request.ItemDescriptionRequest import ItemDescriptionRequest

import unittest

class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        
        item = ItemDatabase.getItemFromName("olive")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEquals(itemData["isCookingIngredient"], True)
        self.assertEquals(itemData["isCocktailcraftingIngredient"], True)
        self.assertEquals(itemData["image"], "olive.gif")
        self.assertEquals(itemData["autosell"], 35)
        self.assertEquals(itemData["type"], "food")
        
        item = ItemDatabase.getItemFromName("furry fur")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEquals(itemData["isMeatsmithingComponent"], True)
        self.assertEquals(itemData["image"], "furfur.gif")
        self.assertEquals(itemData["autosell"], 129)
        
        item = ItemDatabase.getItemFromName("baconstone")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEquals(itemData["isJewelrymakingComponent"], True)
        self.assertEquals(itemData["image"], "baconstone.gif")
        self.assertEquals(itemData["autosell"], 500)
        
        # Test a haiku item -- these description pages are formatted differently.
        r = ItemDescriptionRequest(s, 435365663)
        itemData = r.doRequest()
        self.assertEquals(itemData["name"], "little round pebble")
        self.assertEquals(itemData["autosell"], 45)
        self.assertEquals(itemData["type"], "off-hand item")
