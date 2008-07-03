from kol.request.GetMessagesRequest import GetMessagesRequest

class InventoryManager(object):
	"""
	This class manages a user's inventory.
	"""
	
	def __init__(self, session):
		"Initializes the InventoryManager with a particular KoL session."
		self.session = session
		session.inventoryManager = self
	
	def refreshInventory(self):
		
	def addItem(self, item):
		
	def removeItem(self, item):
		
