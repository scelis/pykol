import kol.Error as Error
from kol.util import Report
from kol.manager import PatternManager
from GenericRequest import GenericRequest

import time

class StoreGetTransactions(GenericRequest):
	"""
	Get the last 2 weeks of transactions from your store.

	Fields:
	timestamp:		time of the sale
	userId: 		userID of purchasee
	userName: 		Username of purchasee
	quantiy:		Quantity sold
	name:			Name of item sold
	meat:			Meat earned by transaction
	11/06/13 21:32:51
	"""

	def __init__(self, session):
		super(StoreGetTransactions, self).__init__(session)
		self.url = session.serverURL + 'backoffice.php'
		self.requestData['which'] = 3
		self.requestData['pwd'] = session.pwd

	def parseResponse(self):
		sales = []
		mallSalesPattern = PatternManager.getOrCompilePattern('mallTransactions')
		for match in mallSalesPattern.finditer(self.responseText):
			sale = {}
			sale["timestamp"] = time.strptime(match.group(1), '%m/%d/%y %H:%M:%S')
			sale["userid"] = int(match.group(2))
			sale["userName"] = str(match.group(3))
			sale["quantity"] = int(match.group(4))
			sale["name"] = str(match.group(5))
			sale["meat"] = int(match.group(6))
			sales.append(sale)
		self.responseData["mallSales"] = sales
