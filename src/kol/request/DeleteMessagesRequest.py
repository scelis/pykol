from GenericRequest import GenericRequest

class DeleteMessagesRequest(GenericRequest):
	"A request used to delete messages."
	
	def __init__(self, session, messagesToDelete, box="Inbox"):
		super(DeleteMessagesRequest, self).__init__(session)
		self.url = session.serverURL + "messages.php"
		self.requestData["the_action"] = "delete"
		self.requestData["pwd"] = session.pwd
		self.requestData["box"] = box
		
		for msgId in messagesToDelete:
			self.requestData["sel%s" % msgId] = "1"
