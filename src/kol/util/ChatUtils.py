from kol.manager import PatternManager
from kol.util import StringUtils

def parseMessages(text):
	# Prepare the patterns.
	htmlCommentPattern = PatternManager.getOrCompilePattern("htmlComment")
	channelPattern = PatternManager.getOrCompilePattern("chatChannel")
	chatPattern = PatternManager.getOrCompilePattern("chatMessage")
	emotePattern = PatternManager.getOrCompilePattern("chatEmote")
	privateChatPattern = PatternManager.getOrCompilePattern("privateChat")
	newKmailPattern = PatternManager.getOrCompilePattern("chatNewKmailNotification")
	
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
				chat["text"] = StringUtils.htmlEntityDecode(match.group(3)).strip()
				parsedChat = True
		
		# See if this was an emote.
		if parsedChat == False:
			match = emotePattern.search(line)
			if match:
				chat["type"] = "emote"
				chat["userId"] = int(match.group(1))
				chat["userName"] = match.group(2)
				chat["text"] = StringUtils.htmlEntityDecode(match.group(3)).strip()
				parsedChat = True
				
		# See if this was a private message.
		if parsedChat == False:
			match = privateChatPattern.search(line)
			if match:
				chat["type"] = "private"
				chat["userId"] = int(match.group(1))
				chat["userName"] = match.group(2)
				chat["text"] = StringUtils.htmlEntityDecode(match.group(3)).strip()
				parsedChat = True
		
		# See if this is a new kmail notification.
		if parsedChat == False:
			match = newKmailPattern.search(line)
			if match:
				chat["type"] = "notification:kmail"
				chat["userId"] = int(match.group(1))
				chat["userName"] = match.group(2)
				parsedChat = True
		
		# Handle unrecognized chat messages.
		if parsedChat == False:
			chat["type"] = "unknown"
			chat["text"] = StringUtils.htmlEntityDecode(line)
			
		chats.append(chat)
	
	return chats
