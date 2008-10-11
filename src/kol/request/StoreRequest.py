from GenericRequest import GenericRequest
from kol.Error import RequestError, NotEnoughMeatError, NotSoldHereError, NotAStoreError, UserShouldNotBeHereError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class StoreRequest(GenericRequest):
	"Purchases items from a store."
	
	SMACKETERIA = '3'
	GOUDAS_GRIMOIRE_AND_GROCERY = '2'
	SHADOWY_STORE = '1'
	LABORATORY = 'g'
	BLACK_MARKET = 'l'
	WHITE_CITADEL = 'w'
	BAKERY = '4'
	GENERAL_STORE = '5'
	LITTLE_CANADIA_JEWELERS = 'j'
	GNO_MART = 'n'
	NERVEWRECKERS = 'y'
	ARMORY_AND_LEGGERY = 'z'
	BUGBEAR_BAKERY = 'b'
	MARKET = 'm'
	MEATSMITH = 's'
	BARTELBYS_BARGAIN_BOOKSTORE = 'r'
	HIPPY_PRODUCE_STAND = 'h'
	UNCLE_PS_ANTIQUES = 'p'

	def __init__(self, session, store, item, quantity=1):
		super(StoreRequest, self).__init__(session)
		self.url = session.serverURL + "store.php"
		self.requestData['phash'] = session.pwd
		self.requestData['whichstore'] = store
		self.requestData['buying'] = "Yep."
		self.requestData['howmany'] = quantity
		self.requestData['whichitem'] = item
				
	def parseResponse(self):
		# Check for errors.
		notEnoughMeatPattern = PatternManager.getOrCompilePattern('noMeatForStore')
		invalidStorePattern = PatternManager.getOrCompilePattern('invalidStore')
		notSoldPattern = PatternManager.getOrCompilePattern('notSoldHere')
		if len(self.responseText) == 0:
			raise UserShouldNotBeHereError("You cannot visit that store yet.")
		if invalidStorePattern.search(self.responseText):
			raise NotAStoreError("The store you tried to visit doesn't exist.")
		if notSoldPattern.search(self.responseText):
			raise NotSoldHereError("This store doesn't carry that item.")
		if notEnoughMeatPattern.search(self.responseText):
			raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")
		
		items = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
		if len(items) == 0:
			raise RequestError("Unknown error. No items received.")
		self.responseData["items"] = items
		
		meatSpentPattern = PatternManager.getOrCompilePattern('meatSpent')
		match = spentMeatPattern.search(self.responseText)
		self.responseData['meatSpent'] = int(match.group(1).replace(',', ''))
