from GenericRequest import GenericRequest

class AddItemsToDisplayCaseRequest(GenericRequest):
	"Adds items to the player's display case."
	
	def __init__(self, session, items):
		super(AddItemsToDisplayCaseRequest, self).__init__(session)
		self.url = session.serverURL + "managecollection.php"
		self.requestData["pwd"] = session.pwd
		self.requestData["action"] = "put"
		
		ctr = 0
		for item in items:
			ctr += 1
			self.requestData["whichitem%s" % ctr] = item["id"]
			self.requestData["howmany%s" % ctr] = item["quantity"]
