from GenericRequest import GenericRequest
from kol.util import ChatUtils

import time
import urllib

class SendChatRequest(GenericRequest):
	def __init__(self, session, text):
		super(SendChatRequest, self).__init__(session)
		self.text = text.strip()
		self.url = session.serverURL + "submitnewchat.php?playerid=%s&pwd=%s" % (session.userId, session.pwd)
		self.url += "&%s" % urllib.urlencode({"graf":text})
	
	def parseResponse(self):
		# Parse the chat messages returned.
		self.responseData["chatMessages"] = ChatUtils.parseMessages(self.responseText)
		
		# Sleep otherwise the server might display chat messages out of order if we send
		# a bunch in a row.
		time.sleep(2)
		