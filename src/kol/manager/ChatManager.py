from kol.manager import PatternManager
from kol.request.GetChatMessagesRequest import GetChatMessagesRequest
from kol.request.OpenChatRequest import OpenChatRequest
from kol.request.SendChatRequest import SendChatRequest

import time

MAX_CHAT_LENGTH = 200

class ChatManager(object):
	"This class can be used as an interface for KoL chat."
	
	def __init__(self, session):
		"Initializes the ChatManager with a particular KoL session and then connects to chat."
		self.session = session
		self.lastRequestTimestamp = 0
		session.chatManager = self
		r = OpenChatRequest(self.session)
		data = r.doRequest()
		self.currentChannel = data["currentChannel"]
		
	def getNewChatMessages(self):
		r = GetChatMessagesRequest(self.session, self.lastRequestTimestamp)
		data = r.doRequest()
		self.lastRequestTimestamp = data["lastSeen"]
		chats = data["chatMessages"]
		
		# Set the channel in each channel-less chat to be the current channel.
		for chat in chats:
			t = chat["type"]
			if t == "normal" or t == "emote":
				if "channel" not in chat:
					chat["channel"] = self.currentChannel
		
		return chats
	
	def sendChatMessage(self, text):
		messages = []
		
		# Clean the text.
		text = text.strip()
		whitespacePattern = PatternManager.getOrCompilePattern('whitespace')
		text = whitespacePattern.sub(' ', text)
		
		if len(text) > MAX_CHAT_LENGTH:
			# We need to break up the chat message into chunks.
			arr = text.split(' ')
			
			# First, let's see if there is a prefix that should be appended to each
			# chat message we send to the server.
			prefix = ''
			if arr[0].lower() in ["/msg", "/whisper", "/w", "/tell"] and len(arr) > 2:
				prefix = "/w %s " % arr[1]
				text = ' '.join(arr[2:])
			elif arr[0].find('/') == 0:
				prefix = arr[0] + ' '
				text = ' '.join(arr[1:])
			
			# Construct the array of messages to send.
			while len(text) > (MAX_CHAT_LENGTH - len(prefix)):
				index = text.rfind(" ", 0, MAX_CHAT_LENGTH - len(prefix) - 6)
				if index == -1:
					index = MAX_CHAT_LENGTH - len(prefix) - 6
					msg = text[:index] + "..."
					text = text[index:]
				else:
					msg = text[:index] + "..."
					text = text[index+1:]
				
				if len(messages) > 0:
					msg = "..." + msg
				messages.append(prefix + msg)
				
			if len(messages) > 0:
				messages.append(prefix + "..." + text)
			else:
				messages.append(prefix + text)
		else:
			messages.append(text)
		
		# Send the message(s).
		chats = []
		for message in messages:
			r = SendChatRequest(self.session, message)
			data = r.doRequest()
			tmpChats = data["chatMessages"]
			for chat in tmpChats:
				chats.append(chat)
		
		return chats
