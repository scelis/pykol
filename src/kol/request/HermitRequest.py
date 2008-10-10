from kol.Error import RequestError, NotEnoughItemsError, NotEnoughHermitPermitsError, NotSoldHereError
from kol.util import ParseResponseUtils
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

"""
Need to check when requesting an item he doesn't have as well
"""

class HermitRequest(GenericRequest):

	def __init__(self, session, item, quantity=1):
		super(HermitRequest, self).__init__(session)
		self.session = session
		self.url = session.serverURL + "hermit.php"
		self.requestData['action'] = "trade"
		self.requestData['quantity'] = quantity
		self.requestData['whichitem'] = item
				
	def parseResponse(self):
		notEnoughCloversPattern = PatternManager.getOrCompilePattern('notEnoughClovers')
		noTrinketsPattern = PatternManager.getOrCompilePattern('noTrinkets')
		noHermitPermitPattern = PatternManager.getOrCompilePattern('noHermitPermits')
		notHermitItemPattern = PatternManager.getOrCompilePattern('notHermitItem')
		
		# Check for errors.
		if notEnoughCloversPattern.search(self.responseText):
			raise RequestError("The Hermit doesn't have enough clovers for that")
		if noTrinketsPattern.search(self.responseText):
			raise NotEnoughItemsError("You don't have enough worthless items for that")
		if noHermitPermitPattern.search(self.responseText):
			raise NotEnoughHermitPermitsError("You don't have enough hermit permits for that")
		if notHermitItemPattern.search(self.responseText):
			raise NotSoldHereError("The Hermit doesn't have any of those")
		
		response = {}
		
		items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
		if len(items) > 0:
			response["items"] = items
		
		self.responseData = response