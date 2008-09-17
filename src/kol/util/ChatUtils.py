from kol.manager import PatternManager
from kol.util import Report
from kol.util import StringUtils

CHAT_CHANNELS = [
	"clan",
	"dev",
	"foodcourt",
	"games",
	"haiku",
	"hardcore",
	"harem",
	"hobopolis",
	"kwe",
	"lounge",
	"mod",
	"newbie",
	"normal"
	"pvp",
	"radio",
	"trade",
	"valhalla",
	"veteran",
	"villa",
]

def parseMessages(text, isGet):
	# Prepare the patterns.
	htmlCommentPattern = PatternManager.getOrCompilePattern("htmlComment")
	htmlTagPattern = PatternManager.getOrCompilePattern("htmlTag")
	channelPattern = PatternManager.getOrCompilePattern("chatChannel")
	chatPattern = PatternManager.getOrCompilePattern("chatMessage")
	emotePattern = PatternManager.getOrCompilePattern("chatEmote")
	privateChatPattern = PatternManager.getOrCompilePattern("privateChat")
	newKmailPattern = PatternManager.getOrCompilePattern("chatNewKmailNotification")
	linkPattern = PatternManager.getOrCompilePattern("chatLink")
	chatWhoPattern = PatternManager.getOrCompilePattern("chatWhoResponse")
	linkedPlayerPattern = PatternManager.getOrCompilePattern("chatLinkedPlayer")
	
	# Get the chat messages.
	chats = []
	lines = text.split("<br>")
		
	for line in lines:
		line = htmlCommentPattern.sub('', line)
		line = line.strip()
		if len(line) == 0:
			continue
		
		chat = {}
		parsedChat = False
		
		# See if this message was posted to a different channel.
		match = channelPattern.search(line)
		if match:
			chat["channel"] = match.group(1)
			line = line[len(match.group(0)):]
		
		# See if this was a normal chat message.
		if parsedChat == False:
			match = chatPattern.search(line)
			if match:
				chat["type"] = "normal"
				chat["userId"] = int(match.group(1))
				chat["userName"] = match.group(2)
				chat["text"] = match.group(3).strip()
				parsedChat = True
		
		# See if this was an emote.
		if parsedChat == False:
			match = emotePattern.search(line)
			if match:
				chat["type"] = "emote"
				chat["userId"] = int(match.group(1))
				chat["userName"] = match.group(2)
				chat["text"] = match.group(3).strip()
				parsedChat = True
		
		if isGet:
			# See if this was a private message.
			if parsedChat == False:
				match = privateChatPattern.search(line)
				if match:
					chat["type"] = "private"
					chat["userId"] = int(match.group(1))
					chat["userName"] = match.group(2)
					chat["text"] = match.group(3).strip()
					parsedChat = True
			
			# See if this is a new kmail notification.
			if parsedChat == False:
				match = newKmailPattern.search(line)
				if match:
					chat["type"] = "notification:kmail"
					chat["userId"] = int(match.group(1))
					chat["userName"] = match.group(2)
					parsedChat = True
			
		else:
			# See if this is a /who response.
			if parsedChat == False:
				if chatWhoPattern.search(line):
					chat["type"] = "who"
					chat["users"] = []
					chatWhoPersonPattern = PatternManager.getOrCompilePattern("chatWhoPerson")
					for match in chatWhoPersonPattern.finditer(line):
						userId = match.group(1)
						userName = match.group(2)
						chat["users"].append({"userId":userId, "userName":userName})
					parsedChat = True
		
		if parsedChat and "text" in chat:
			# Parse user links.
			chat["text"] = linkedPlayerPattern.sub(r'\2', chat["text"])
		
			# Parse misc links.
			match = linkPattern.search(chat["text"])
			while match != None:
				url = match.group(1)
				urlIndex = 0
				textStart = match.end()
				textEnd = textStart
				found = False
				while found == False:
					if chat["text"][textEnd] == url[urlIndex]:
						textEnd += 1
						urlIndex += 1
					elif chat["text"][textEnd] == ' ':
						textEnd += 1
						
					if urlIndex == len(url) - 1:
						found = True
				
				newText = chat["text"][:match.start()] + url + chat["text"][textEnd+1:]
				chat["text"] = newText
				match = linkPattern.search(chat["text"])
			
			# Decode HTML entities.
			chat["text"] = StringUtils.htmlEntityDecode(chat["text"])
		
			# Clean up the text.
			chat["text"] = htmlTagPattern.sub('', chat["text"])
		
		# Handle unrecognized chat messages.
		if parsedChat == False:
			chat["type"] = "unknown"
			chat["text"] = StringUtils.htmlEntityDecode(line)
			
		chats.append(chat)
	
	return chats

def cleanChatMessageToSend(text):
	"Cleans a chat message by removing extra whitespace."
	text = text.strip()
	whitespacePattern = PatternManager.getOrCompilePattern('whitespace')
	text = whitespacePattern.sub(' ', text)
	return text

def parseChatMessageToSend(text):
	"This function assumes that the text has already been cleaned using cleanChatMessageToSend()."
	
	# We need to break up the chat message into chunks.
	arr = text.split(' ')
	lowerText = text.lower()
	chatInfo = {}
	
	if arr[0].find('/') == 0:
		if arr[0] in ["/msg", "/whisper", "/w", "/tell"] and len(arr) > 2:
			chatInfo["type"] = "private"
			chatInfo["recipient"] = arr[1]
		elif arr[0][1:] in CHAT_CHANNELS:
			chatInfo["type"] = "channel"
			chatInfo["channel"] = arr[0][1:]
			if len(arr) > 2 and arr[0] in ["/me", "/em"]:
				chatInfo["isEmote"] = True
		elif arr[0] in ["/me", "/em"]:
			chatInfo["type"] = "channel"
			chatInfo["isEmote"] = True
	else:
		chatInfo["type"] = "channel"
	
	return chatInfo
