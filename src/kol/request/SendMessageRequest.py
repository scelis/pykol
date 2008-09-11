from GenericRequest import GenericRequest
from kol.Error import Error, NotEnoughItemsError, UserInHardcoreRoninError, UserIsIgnoringError
from kol.manager import PatternManager

class SendMessageRequest(GenericRequest):
	def __init__(self, session, message):
		super(SendMessageRequest, self).__init__(session)
		self.url = session.serverURL + "sendmessage.php?toid="
		self.requestData['action'] = 'send'
		self.requestData['pwd'] = session.pwd
		self.requestData['towho'] = message["userId"]
		self.requestData['message'] = message["text"]
		self.requestData['savecopy'] = "on"
		
		# Add the items to the message.
		if "items" in message and len(message["items"]) > 0:
			i = 1
			for item in message["items"]:
				self.requestData['whichitem%s' % i] = item["id"]
				self.requestData['howmany%s' % i] = item["quantity"]
				i += 1
		
		# Add meat to the message.
		if "meat" in message:
			self.requestData["sendmeat"] = message["meat"]
		else:
			self.requestData["sendmeat"] = 0
	
	def parseResponse(self):
		hardcoreRoninPattern = PatternManager.getOrCompilePattern('userInHardcoreRonin')
		ignoringPattern = PatternManager.getOrCompilePattern('userIgnoringUs')
		notEnoughItemsPattern = PatternManager.getOrCompilePattern('notEnoughItemsToSend')
		if hardcoreRoninPattern.search(self.responseText):
			raise UserInHardcoreRoninError("Unable to send items or meat. User is in hardcore or ronin.")
		elif ignoringPattern.search(self.responseText):
			raise UserIsIgnoringError("Unable to send message. User is ignoring us.")
		elif notEnoughItemsPattern.search(self.responseText):
			raise NotEnoughItemsError("You don't have enough of one of the items you're trying to send.")
