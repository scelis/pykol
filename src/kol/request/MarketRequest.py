from kol.Error import RequestError, NotEnoughMeatError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

availableItems = [2595, 744, 23, 829, 61, 69, 1631, 530, 247, 1003, 40, 42, 16, 14, 15, 274, 1261, 236, 157, 3128, 2945, 1080, 2681, 2680, 2679, 3235, 3233, 3234]

class MarketRequest(GenericRequest):

	def __init__(self, session, item, quantity=1):
		super(MarketRequest, self).__init__(session)
		self.url = session.serverURL + "store.php"
		self.requestData['phash'] = session.pwd
		self.requestData['whichstore'] = 'm'
		self.requestData['buying'] = "Yep."
		self.requestData['howmany'] = quantity
		
		if item in availableItems:
			self.requestData['whichitem'] = item
		else:
			raise RequestError("That item isn't available at the Market Square.")
				
	def parseResponse(self):
		notEnoughMeatPattern = PatternManager.getOrCompilePattern('noMeatForStore')
		meatSpentPattern = PatternManager.getOrCompilePattern('meatSpent')
		singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
		multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
		
		# Check for errors.
		if noteEnoughMeatPattern.search(self.responseText):
			raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")
		
		response={}
		
		# Find out how much meat was spent
		match = meatSpentPattern.search(self.responseText)
		if match:
				meatSpent = int(match.group(1).replace(',', ''))
				response["meatSpent"] = meatSpent
		
		# Find items recieved, if any.
		items = []
		for match in singleItemPattern.finditer(self.responseText):
			descId = int(match.group(1))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = 1
			items.append(item)
		for match in multiItemPattern.finditer(self.responseText):
			descId = int(match.group(1))
			quantity = int(match.group(2).replace(',', ''))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = quantity
			items.append(item)
		if len(items) > 0:
			response["item"] = items
		
		self.responseData = response