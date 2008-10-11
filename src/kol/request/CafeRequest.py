from GenericRequest import GenericRequest
from kol.Error import NotEnoughMeatError, NotSoldHereError,  UserShouldNotBeHereError
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class CafeRequest(GenericRequest):
	"Purchases items from a cafe."
	
	CHEZ_SNOOTEE ='1'
	MICROBREWERY = '2'
	HELLS_KITCHEN = '3'
	
	def __init__(self, session, cafe, item):
		super(CafeRequest, self).__init__(session)
		self.session = session
		self.url = session.serverURL + "cafe.php"
		self.requestData['pwd'] = session.pwd
		self.requestData['cafeid'] = cafe
		self.requestData['action'] = "CONSUME!"
		self.requestData['whichitem'] = item
				
	def parseResponse(self):
		# Check for errors.
		notEnoughMeatPattern = PatternManager.getOrCompilePattern('noMeatForStore')
		cannotGoPattern = PatternManager.getOrCompilePattern('userShouldNotBeHere')
		notSoldPattern = PatternManager.getOrCompilePattern('notSoldHere')

		if cannotGoPattern.search(self.responseText):
			raise UserShouldNotBeHereError("You cannot reach that cafe")
		if notSoldPattern.search(self.responseText):
			raise NotSoldHereError("This cafe doesn't carry that item.")
		if notEnoughMeatPattern.search(self.responseText):
			raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")
				
		response = {}

		advResponse = ParseResponseUtils.parseAdventuresGained(self.responseText)
		if advResponse > 0:
			response["adventures"] = advResponse

		drunkResponse = ParseResponseUtils.parseDrunkGained(self.responseText)
		if drunkResponse > 0:
			response["drunkeness"] = drunkResponse

		subResponse = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)
		if len(subResponse) > 0:
			response["substats"] = subResponse

		statResponse = ParseResponseUtils.parseStatsGainedLost(self.responseText)
		if len(statResponse) > 0:
			response["statPoints"] = statResponse

		levelResponse = ParseResponseUtils.parseLevelsGained(self.responseText)
		if levelResponse > 0:
			response["level"] = levelResponse

		effectResponse = ParseResponseUtils.parseEffectsGained(self.responseText)
		if len(effectResponse) > 0:
			response["effects"] = effectResponse

		hpResponse = ParseResponseUtils.parseHPGainedLost(self.responseText)
		if hpResponse != 0:
			reponse["hp"] = hpResponse
		
		mpResponse = ParseResponseUtils.parseMPGainedLost(self.responseText)
		if mpResponse != 0:
			reponse["mp"] = mpResponse

		self.responseData = response
