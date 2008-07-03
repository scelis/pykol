from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ItemDescriptionRequest(GenericRequest):
	def __init__(self, session, descId):
		super(ItemDescriptionRequest, self).__init__(session)
		self.url = session.serverURL + "desc_item.php?whichitem=%s" % descId
		
	def addInformationToItem(self, item):
		if "name" not in item:
			item["name"] = self.getItemName()
		
		image = self.getImage()
		if image != None:
			item["image"] = self.getImage()
		
		itemType = self.getItemType()
		if itemType != None:
			item["type"] = itemType
		
		autosell = self.getAutosellValue()
		if autosell > 0:
			item["autosell"] = autosell
		
		if self.isCookingIngredient():
			item["isCookingIngredient"] = True
		
		if self.isCocktailcraftingIngredient():
			item["isCocktailcraftingIngredient"] = True
		
		if self.isMeatsmithingComponent():
			item["isMeatsmithingComponent"] = True
		
		if self.isJewelrymakingComponent():
			item["isJewelrymakingComponent"] = True
	
	def getItemName(self):
		itemNamePattern = PatternManager.getOrCompilePattern("itemName")
		match = itemNamePattern.search(self.responseText)
		return match.group(1)
	
	def getImage(self):
		imagePattern = PatternManager.getOrCompilePattern("itemImage")
		match = imagePattern.search(self.responseText)
		return match.group(1)
		
	def getItemType(self):
		typePattern = PatternManager.getOrCompilePattern("itemType")
		match = typePattern.search(self.responseText)
		if match:
			return match.group(1)
		return None

	def getAutosellValue(self):
		autosellPattern = PatternManager.getOrCompilePattern("itemAutosell")
		match = autosellPattern.search(self.responseText)
		if match:
			return int(match.group(1))
		else:
			return 0
		
	def isCookingIngredient(self):
		cookingPattern = PatternManager.getOrCompilePattern("isCookingIngredient")
		match = cookingPattern.search(self.responseText)
		if match:
			return True
		return False
	
	def isCocktailcraftingIngredient(self):
		cocktailcraftingPattern = PatternManager.getOrCompilePattern("isCocktailcraftingIngredient")
		match = cocktailcraftingPattern.search(self.responseText)
		if match:
			return True
		return False
	
	def isMeatsmithingComponent(self):
		meatsmithingPattern = PatternManager.getOrCompilePattern("isMeatsmithingComponent")
		match = meatsmithingPattern.search(self.responseText)
		if match:
			return True
		return False
	
	def isJewelrymakingComponent(self):
		jewelrymakingPattern = PatternManager.getOrCompilePattern("isJewelrymakingComponent")
		match = jewelrymakingPattern.search(self.responseText)
		if match:
			return True
		return False
