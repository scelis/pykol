from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils
from kol.Error import NotEnoughItemsError, InvalidActionError, TooFullError

class EatFoodRequest(GenericRequest):
	"""
	This class is for eating food from the inventory.
	It accepts the current session and the ID number of the food to eat.
	It returns the results, including and stat gain, adventure gain, or effect gain.
	"""
	
	def __init__(self, session, foodId):
		super(EatFoodRequest, self).__init__(session)
		self.url = session.serverURL + "inv_eat.php?pwd=" + session.pwd + "&which=1&whichitem=" + str(foodId)
		
	def parseResponse(self):
		# Check for errors
		tooFullPattern = PatternManager.getOrCompilePattern('tooFull')
		if tooFullPattern.search(self.responseText):
			raise TooFullError("You are too full to eat that.")
		notFoodPattern = PatternManager.getOrCompilePattern('notFood')
		if notFoodPattern.search(self.responseText):
			raise InvalidActionError("That item is not food")
		foodMissingPattern = PatternManager.getOrCompilePattern('notEnoughItems')
		if foodMissingPattern.search(self.responseText):
		 raise NotEnoughItemsError("Item not in inventory")

		# Check the results
		results = {}
		
		results["adventures"] = ParseResponseUtils.parseAdventuresGained(self.responseText)
		
		substats = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)
		if len(substats) > 0:
			results["substats"] = substats
		stats = ParseResponseUtils.parseStatsGainedLost(self.responseText)
		if len(stats) > 0:
			results["stats"] = stats
		level = ParseResponseUtils.parseLevelsGained(self.responseText)
		if level != 0:
			results["level"] = level
		hp = ParseResponseUtils.parseHPGainedLost(self.responseText)
		if hp != 0:
			results["hp"] = hp
		mp = ParseResponseUtils.parseMPGainedLost(self.responseText)
		if mp != 0:
			results["mp"] = mp
		effects = ParseResponseUtils.parseEffectsGained(self.responseText)
		if len(effects) > 0:
			results["effects"] = effects
		
		self.responseData = results
		
