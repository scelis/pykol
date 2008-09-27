from kol.Error import RequestError, NotEnoughMeatError, NotEnoughItemsError, NotAStoreError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

"""
The cafes and other specialty store cannot be accessed via this,
as they use different php files

##cafe.php
#CHEZSNOOTEE = 1
#MICROBREWERY = 2
#HELLSKITCHEN = 3

##Doc Galaktik galaktik.php
##Gift Shop town_giftshop.php
##Mr. Store mrstore.php
##The Trophy Hut trophy.php
##Raffle House raffle.php
##Bounty Hunter Hut bhh.php
##Goofballs town_wrong.php?place=goofballs
"""

class StoreRequest(GenericRequest):
	##These can all be used to reference the stores
	MUSCLEGUILD = '3'
	MYSTGUILD = '2'
	MOXIEGUILD = '1'
	LABORATORY = 'g'
	BLACKMARKET = 'l'
	WHITECITADEL = 'w'
	THEBAKERY = '4'
	GENERALSTORE = '5'
	JEWELERS = 'j'
	GNOMART = 'n'
	NERVEWRECKERS = 'y'
	ARMORYLEGGERY = 'z'
	BUGBEARBAKERY = 'b'
	MARKET = 'm'
	MEATSMITH = 's'
	BARTELBYS = 'r'
	HIPPYSTAND = 'h'
	PSANTIQUES = 'p'

	def __init__(self, session, store, item, quantity=1):
		super(StoreRequest, self).__init__(session)
		self.url = session.serverURL + "store.php"
		self.requestData['phash'] = session.pwd
		self.requestData['whichstore'] = store
		self.requestData['buying'] = "Yep."
		self.requestData['howmany'] = quantity
		self.requestData['whichitem'] = item
				
	def parseResponse(self):
		notEnoughMeatPattern = PatternManager.getOrCompilePattern('noMeatForStore')
		meatSpentPattern = PatternManager.getOrCompilePattern('meatSpent')
		invalidStorePattern = PatternManager.getOrCompilePattern('invalidStore')
		notSoldPattern = PatternManager.getOrCompilePattern('notSoldHere')
		singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
		multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
		
		# Check for errors.
		if invalidStorePattern.search(self.responseText):
			raise NotAStoreError("The store you tried to visit doesn't exist.")
		if notSoldPattern.search(self.responseText):
			raise NotEnoughItemsError("The store doesn't carry that item.")
		if notEnoughMeatPattern.search(self.responseText):
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