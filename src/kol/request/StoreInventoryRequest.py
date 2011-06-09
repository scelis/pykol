import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import StringUtils

class StoreInventoryRequest(GenericRequest):
        "This class is used to get a list of items currently in a user's store"

        def __init__(self, session):
                super(StoreInventoryRequest, self).__init__(session)
                self.url = session.serverURL + 'managestore.php'

	def parseResponse(self):
		storeInventoryPattern = PatternManager.getOrCompilePattern('storeInventory')

		items = []

		for item in storeInventoryPattern.finditer(self.responseText):
			name = item.group(1)
			if item.group(2) == None:
				amnt = 1
			else:
				amnt = int(item.group(2))
			price = item.group(3)
			if item.group(4) == '<font size=1>(unlimited)</font>&nbsp;&nbsp;':
				limit = 0
			else:
				limit = item.group(4)	
			m = {"item":name, "amnt":amnt, "price":price, "limit":limit}
			items.append(m)

		self.responseData["items"] = items
