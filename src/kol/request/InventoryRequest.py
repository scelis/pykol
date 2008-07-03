from GenericRequest import GenericRequest
from kol.Error import ItemNotFoundError
from kol.database import ItemDatabase
from kol.manager import PatternManager

class InventoryRequest(GenericRequest):
	"""
	This class is used to get a list of items in the user's inventory
	"""
	
	def __init__(self, session, which=None):
		super(InventoryRequest, self).__init__(session)
		self.url = session.serverURL + "inventory.php"
		if which != None:
			self.url += "?which=%s" % which
	
	def getItems(self):
		items = []
		
		singleItemPattern = PatternManager.getOrCompilePattern('inventorySingleItem')
		for match in singleItemPattern.finditer(self.responseText):
			descId = int(match.group(1))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = 1
			items.append(item)
			
		multipleItemsPattern = PatternManager.getOrCompilePattern('inventoryMultipleItems')
		for match in multipleItemsPattern.finditer(self.responseText):
			descId = int(match.group(1))
			quantity = int(match.group(3))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = quantity
			items.append(item)
		
		return items
