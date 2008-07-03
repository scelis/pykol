from GenericRequest import GenericRequest

import urllib

class SendChatRequest(GenericRequest):
	def __init__(self, session, text):
		super(SendChatRequest, self).__init__(session)
		self.text = text.strip()
		self.url = session.serverURL + "submitnewchat.php?playerid=%s&pwd=%s" % (session.userId, session.pwd)
		
	def doRequest(self):
		text = self.text
		messages = []
		
		# We need to break up the message if it is too big.
		while len(text) > 194:
			index = text.rfind(" ", 0, 193)
			msg = text[:index] + "..."
			if len(messages) > 0:
				msg = "..." + msg
			messages.append(msg)
			text = text[index+1:]
		if len(messages) > 0:
			messages.append("..." + text)
		else:
			messages.append(text)
		
		# Send the messages
		url = self.url
		for message in messages:
			m = {"graf":message}
			graf = urllib.urlencode(m)
			self.url = url + "&" + graf
			super(SendChatRequest, self).doRequest()
