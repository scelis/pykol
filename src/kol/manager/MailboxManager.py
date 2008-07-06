from kol.request.GetMessagesRequest import GetMessagesRequest
from kol.request.InventoryRequest import InventoryRequest
from kol.request.UseItemRequest import UseItemRequest

class MailboxManager(object):
	"""
	This class manages a user's mailbox. It can be used as a wrapper to GetMessagesRequest to
	provide additional functionality above and beyond just getting a listing of whatever
	is in the user's mailbox.
	"""
	
	__messagesPerPage = None
	__oldestFirst = None
	
	def __init__(self, session):
		"Initializes the MailboxManager with a particular KoL session."
		self.session = session
		session.mailboxManager = self
	
	def setMessagesPerPage(self, messagesPerPage):
		"Sets how many messages the user wants to receive per request."
		if self.__messagesPerPage != messagesPerPage:
			r = GetMessagesRequest(self.session, messagesPerPage=messagesPerPage)
			r.doRequest()
			self.__messagesPerPage = messagesPerPage
		
	def setOldestFirst(self, oldestFirst):
		"Sets whether the user wants their messages sorted oldest first or newest first."
		if self.__oldestFirst != oldestFirst:
			r = GetMessagesRequest(self.session, oldestFirst=oldestFirst)
			r.doRequest()
			self.__oldestFirst = oldestFirst
	
	def getMessages(self, box="Inbox", pageNumber=None, messagesPerPage=None, oldestFirst=None):
		"""
		A wrapper to GetMessagesRequest. Ensures that the user never specifies both messagesPerPage
		and oldestFirst. Doing so can cause the request to be very slow.
		"""
		if messagesPerPage != None:
			self.setMessagesPerPage(messagesPerPage)
		if oldestFirst != None:
			self.setOldestFirst(oldestFirst)
		r = GetMessagesRequest(self.session, box=box, pageNumber=pageNumber)
		responseData = r.doRequest()
		return responseData["kmails"]
	
	def getAllMessages(self, box="Inbox", openGiftPackages=False, removeGiftPackages=False):
		"""
		Gets all messages in the user's box. This method also supports the notion of automatically
		opening gift packages. In addition, these gift packages can be removed from the item array
		in each message.
		"""
		# To speed up the request, make sure we are requesting 100 messages per page.
		oldMessagesPerPage = self.__messagesPerPage
		if oldMessagesPerPage != 100:
			self.setMessagesPerPage(100)
		
		# Get all messages.
		page = 0
		messages = []
		while len(messages) == page * 100:
			page += 1
			messages.extend(self.getMessages(box=box, pageNumber=page))
		
		# Check to see if we should open gift packages.
		if openGiftPackages:
			
			# First get a list of messages that contain potentially unopened gift packages.
			messagesWithUnopenedPackages = []
			for m in messages:
				if len(m["items"]) == 1 and m["meat"] == 0:
					if "type" in m["items"][0] and m["items"][0]["type"] == "gift package":
						messagesWithUnopenedPackages.append(m["id"])
			
			# If there are gift packages, open them and then re-fetch the messages.
			if len(messagesWithUnopenedPackages) > 0:
				self.openAllGiftPackages()
				messages = self.getAllMessages(box=box)
			
				# If any of the messages we saw before still has a gift package that looks
				# unopened, then we are witnessing a known bug in KoL. Apparently it is somehow
				# possible to send a gift package with nothing inside of it. Just delete the
				# package from the message and go on. If a new message has arrived with a gift
				# package, ignore it for now. We can look at it next time.
				messagesToIgnore = []
				for m in messages:
					if len(m["items"]) == 1 and m["meat"] == 0:
						if "type" in m["items"][0] and m["items"][0]["type"] == "gift package":
							if m["id"] in messagesWithUnopenedPackages:
								m["items"] = []
							else:
								messagesToIgnore.append(m)
				for m in messagesToIgnore:
					messages.remove(m)
		
		# Check to see if we should remove gift packages from the messages.
		if removeGiftPackages:
			for m in messages:
				for item in m["items"]:
					if "type" in item and item["type"] == "gift package":
						m["items"].remove(item)
		
		# Revert to our old value for messagesPerPage.
		if oldMessagesPerPage != self.__messagesPerPage:
			self.setMessagesPerPage(oldMessagesPerPage)
		
		return messages
	
	def openAllGiftPackages(self):
		giftPackages = {}
		
		# Get a list of all gift packages in our inventory.
		r = InventoryRequest(self.session, which=3)
		responseData = r.doRequest()
		items = responseData["items"]
		for item in items:
			if "type" in item and item["type"] == "gift package":
				giftPackages[item["id"]] = item["quantity"]
		
		# Open all of the gift packages.
		for itemId,quantity in giftPackages.iteritems():
			for i in range(quantity):
				r = UseItemRequest(self.session, itemId)
				r.doRequest()
