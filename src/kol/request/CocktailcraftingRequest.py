from kol.Error import InvalidRecipeError, NotEnoughItemsError, NotEnoughAdventuresLeftError, SkillMissingError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class CocktailcraftingRequest(GenericRequest):

	def __init__(self, session, itemid1, itemid2, numDrinks=1, makeMax=False):
		super(CocktailcraftingRequest, self).__init__(session)
		self.url = session.serverURL + "cocktail.php"
		self.requestData['pwd'] = session.pwd
		self.requestData['action'] = "combine"
		self.requestData['quantity'] = numDrinks
		self.requestData['item1'] = itemid1
		self.requestData['item2'] = itemid2
		
		if makeMax:
			self.requestData['makemax'] = "on"
	
	def parseResponse(self):
		itemsDontMakeCocktailPattern = PatternManager.getOrCompilePattern('itemsDontMakeCocktail')
		dontHaveSkillPattern = PatternManager.getOrCompilePattern('dontHaveSkillToMixCocktail')
		dontHaveItemsPattern = PatternManager.getOrCompilePattern('dontHaveItemsForThatCocktail')
		dontHaveAdventuresPattern = PatternManager.getOrCompilePattern('dontHaveAdventuresToMixCocktail')
		
		# Check for errors.
		if itemsDontMakeCocktailPattern.search(self.responseText):
			raise InvalidRecipeError("Unable to make cocktail. The submitted ingredients do not mix together.")
		elif dontHaveSkillPattern.search(self.responseText):
			raise SkillMissingError("Unable to make cocktail. We are not skilled enough.")
		elif dontHaveItemsPattern.search(self.responseText):
			raise NotEnoughItemsError("Unable to make cocktail. You don't have all of the items you are trying to mix.")
		elif dontHaveAdventuresPattern.search(self.responseText):
			raise NotEnoughAdventuresLeftError("Unable to mix drink(s). We don't have enough adventures.")

		# Find the items attached to the message.
		singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
		match = singleItemPattern.search(self.responseText):
		if match:
			descId = int(match.group(1))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = 1
		else:
			multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
			match = multiItemPattern.finditer(self.responseText):
			if match:
				descId = int(match.group(1))
				item = ItemDatabase.getItemFromDescId(descId, self.session)
				quantity = int(match.group(2).replace(',', ''))
				item["quantity"] = quantity
			else:
				raise RequestError("Unknown error.")
		
		self.responseData["booze"] = item
