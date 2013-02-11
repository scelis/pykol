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
    "slimetube",
    "trade",
    "valhalla",
    "veteran",
    "villa",
]

def parseIncomingChatMessage(text):
    return parseChatMessages(text, True)

def parseOutgoingChatMessages(text):
    return parseChatMessages(text, False)

def parseChatMessages(text, isIncoming):
    """
    This function parses chats passed to it. The chats are assumed to come from a GetChatMessagesRequest.
    Returns a list of chats, each of which is a dictionary possibly containing the following keys:
        "type" : What kind of chat this is.  Current possible values are
            "channel"
            "listen"
            "listen:start"
            "listen:stop"
            "normal"
            "emote"
            "private"
            "system message"
            "mod warning"
            "mod announcement"
            "notification:kmail"
            "unknown"
        "currentChannel" : The current channel as indicated when sending a /c, /s, or /l request
        "otherChannels" : The other channels being listened to as indicated by a /l request
        "description" : The description of the current channel as indicated when sending a /c or /s request
        "channel" : The channel this chat message was posted from
        "userId" : The user id number of the user sending this chat message
        "userName" : The user name of the user sending this chat message
        "text" : The text of the current chat message
        "isMultiline" : A flag indicating whether this is a multiline message such as a haiku or a message from the Gothy Effect
    """
    
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
    multiLinePattern = PatternManager.getOrCompilePattern("chatMultiLineStart")
    multiEmotePattern = PatternManager.getOrCompilePattern("chatMultiLineEmote")
    playerLoggedOnPattern = PatternManager.getOrCompilePattern("chatPlayerLoggedOn")
    playerLoggedOffPattern = PatternManager.getOrCompilePattern("chatPlayerLoggedOff")

    # Get the chat messages.
    chats = []

    # Check for responses to outgoing chat commands.
    if isIncoming == False:
        outPrivatePattern = PatternManager.getOrCompilePattern("outgoingPrivate")
        chatNewChannelPattern = PatternManager.getOrCompilePattern("newChatChannel")
        chatListenPattern = PatternManager.getOrCompilePattern("chatListenResponse")
        chatListenStartPattern = PatternManager.getOrCompilePattern("chatStartListen")
        chatListenStopPattern = PatternManager.getOrCompilePattern("chatStopListen")

        # See if it is an outgoing private message
        match = outPrivatePattern.search(text)
        if match:
            chat = {}
            chat["type"] = "private"
            chat["userName"] = match.group(2)
            chat["userId"] = int(match.group(1))
            chat["text"] = match.group(3).strip()
            text = text[:match.start()] + text[match.end():]
            chats.append(chat)

        # See if the user changed chat channels through /c or /s
        match = chatNewChannelPattern.search(text)
        if match:
            chat = {}
            chat["type"] = "channel"
            chat["currentChannel"] = match.group(1)
            chat["description"] = match.group(2).replace('<br>','')
            text = text[:match.start()] + text[match.end():]
            chats.append(chat)

        # See if it is a /l response
        match = chatListenPattern.search(text)
        if match:
            chat = {}
            listen = match.group()
            currentPattern = PatternManager.getOrCompilePattern("chatListenCurrent")
            otherPattern = PatternManager.getOrCompilePattern("chatListenOthers")
            chat["type"] = "listen"
            chat["currentChannel"] = currentPattern.search(listen).group(1)
            other = []
            for channel in otherPattern.finditer(listen):
                other.append(channel.group(1))
            chat["otherChannels"] = other
            text = text[:match.start()] + text[match.end():]
            chats.append(chat)

        # See if it is a /l <channel> response to start listening to a channel
        match = chatListenStartPattern.search(text)
        if match:
            chat = {}
            chat["type"] = "listen:start"
            chat["channel"] = match.group(1)
            text = text[:match.start()] + text[match.end():]
            chats.append(chat)
        
        # See if it is a /l <channel> response to stop listening to a channel
        match = chatListenStopPattern.search(text)
        if match:
            chat = {}
            chat["type"] = "listen:stop"
            chat["channel"] = match.group(1)
            text = text[:match.start()] + text[match.end():]
            chats.append(chat)

    lines = text.split("<br>")

    for line in lines:
        line = htmlCommentPattern.sub('', line)
        line = line.strip()
        if len(line) == 0:
            continue

        # Mod Announcements and Mod Warnings leave leading </font> tags at the beginning of the next message
        # This method will remove them and also skip the line if that is all there is
        if line[:7] == "</font>":
            if len(line) == 7:
                continue
            else:
                line = line[7:].strip()

        # System Announcements leave leading </b></font> tags at the beginning of the next message
        # This method will remove them and also skip the line if that is all there is
        if line[:11] == "</b></font>":
            if len(line) == 11:
                continue
            else:
                line = line[11:].strip()

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

                # Check for special announcements
                if chat["userId"] == -1 or chat["userName"] == "System Message":
                    chat["type"] = "system message"
                elif chat["userName"] == "Mod Warning":
                    chat["type"] = "mod warning"
                elif chat["userName"] == "Mod Announcement":
                    chat["type"] = "mod announcement"

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

        if isIncoming == True:
            # See if a user logged in.
            if parsedChat == False:
                match = playerLoggedOnPattern.search(line)
                if match:
                    chat["type"] = "logonNotification"
                    chat["userId"] = int(match.group(1))
                    chat["userName"] = match.group(2)
                    parsedChat = True

            # See if a user logged out.
            if parsedChat == False:
                match = playerLoggedOffPattern.search(line)
                if match:
                    chat["type"] = "logoffNotification"
                    chat["userId"] = int(match.group(1))
                    chat["userName"] = match.group(2)
                    parsedChat = True

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

            # See if this is the start of a multi-line message (Gothy or Haiku)
            if parsedChat == False:
                match = multiLinePattern.search(line)
                if match:
                    chat["type"] = "normal"
                    chat["userId"] = int(match.group(1))
                    chat["userName"] = match.group(2)
                    chat["isMultiline"] = True
                    chat["text"] = ""
                    parsedChat = True

            # See if this is the start of a multi-line emote (Gothy or Haiku)
            # I've seen a Haiku emote, don't know if Gothy will trigger for it
            if parsedChat == False:
                match = multiEmotePattern.search(line)
                if match:
                    chat["type"] = "emote"
                    chat["userId"] = int(match.group(1))
                    chat["userName"] = match.group(2)
                    chat["isMultiline"] = True
                    chat["text"] = ""
                    parsedChat = True

        else:
            # See if this is a /who response.
            if parsedChat == False:
                if chatWhoPattern.search(line):
                    chat["type"] = "who"
                    chat["users"] = []
                    chatWhoPersonPattern = PatternManager.getOrCompilePattern("chatWhoPerson")
                    for match in chatWhoPersonPattern.finditer(line):
                        userClass = match.group(1)
                        userId = match.group(2)
                        userName = match.group(3)
                        userInfo = {"userId" : userId, "userName" : userName}
                        if userClass == "afk":
                            userInfo["isAway"] = True
                        chat["users"].append(userInfo)
                    parsedChat = True

        if parsedChat and "text" in chat:
            chat["text"] = cleanChatText(chat["text"])

        # Handle unrecognized chat messages.
        if parsedChat == False:
            # If the last chat was flagged as starting a multiline
            if len(chats) > 0 and "isMultiline" in chats[-1]:
                if chats[-1]["isMultiline"] == True:
                    if len(chats[-1]["text"]) > 0:
                        chats[-1]["text"] += "\n"
                    line = line.replace('<Br>','\n')
                    cleanLine = cleanChatText(line)
                    cleanLine = cleanLine.replace('&nbsp;','').strip()

                    chats[-1]["text"] += cleanLine

                    continue

            # If the last chat was flagged as a System or Mod Announcement, skip past the trailing tags
            elif len(chats) > 0:
                if "type" in chats[-1] and chats[-1]["type"] in ["system message", "mod warning", "mod announcement"]:
                    if line == "</b></font>":
                        continue

            # Any other case we aren't prepared to handle
            Report.error("bot", "Unknown message.  ResponseText = %s" % text)
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

def cleanChatText(dirtyText):
    "This functions parses player links and external links in the body of the chat text, and cleans any html tags"

    linkPattern = PatternManager.getOrCompilePattern("chatLink")
    linkedPlayerPattern = PatternManager.getOrCompilePattern("chatLinkedPlayer")
    htmlTagPattern = PatternManager.getOrCompilePattern("htmlTag")

    text = dirtyText

    # Parse user links.
    text = linkedPlayerPattern.sub(r'\2', text)

    # Parse misc links.
    match = linkPattern.search(text)
    while match != None:
        url = match.group(1)
        urlIndex = 0
        textStart = match.end()
        textEnd = textStart
        found = False
        while found == False:
            if text[textEnd] == url[urlIndex]:
                textEnd += 1
                urlIndex += 1
            elif text[textEnd] == ' ':
                textEnd += 1

            if urlIndex == len(url):
                found = True

        newText = text[:match.start()] + url + text[textEnd:]
        text = newText
        match = linkPattern.search(text)

    # Decode HTML entities.
    text = StringUtils.htmlEntityDecode(text)

    # Clean up the text.
    text = htmlTagPattern.sub('', text)

    return text
