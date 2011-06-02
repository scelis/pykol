from kol.request.GetChatMessagesRequest import GetChatMessagesRequest
from kol.request.OpenChatRequest import OpenChatRequest
from kol.request.SendChatRequest import SendChatRequest
from kol.util import ChatUtils

import time

MAX_CHAT_LENGTH = 200

class ChatManager(object):
    "This class can be used as an interface for KoL chat."

    def __init__(self, session):
        "Initializes the ChatManager with a particular KoL session and then connects to chat."
        self.session = session
        self.lastRequestTimestamp = 0
        self.lastChatTimestamps = {}
        session.chatManager = self
        r = OpenChatRequest(self.session)
        data = r.doRequest()
        self.currentChannel = data["currentChannel"]

    def getNewChatMessages(self):
        "Gets a list of new chat messages and returns them."
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
        """
        Sends a chat message. This method will throttle chats sent to the same channel or person.
        Otherwise the KoL server could display them out-of-order to other users.
        """
        messages = []

        # Clean the text.
        text = ChatUtils.cleanChatMessageToSend(text)

        # Get information about the chat.
        chatInfo = ChatUtils.parseChatMessageToSend(text)

        if len(text) > MAX_CHAT_LENGTH:

            # Figure out the prefix that should be appended to every message.
            prefix = ''
            if "type" in chatInfo:
                if chatInfo["type"] == "private":
                    prefix = "/w %s " % chatInfo["recipient"]
                elif chatInfo["type"] == "channel":
                    if "channel" in chatInfo:
                        prefix = "/%s " % chatInfo["channel"]
                    if "isEmote" in chatInfo:
                        prefix += "/me "

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
                else:
                    messages.append(msg)

            if len(messages) > 0:
                messages.append(prefix + "..." + text)
            else:
                messages.append(prefix + text)
        else:
            messages.append(text)

        # Determine if we need to throttle the message as we don't want to send two messages
        # to the same person or channel without a little time for the server to figure out
        # which message is first.
        key = None
        lastTime = None
        doThrottle = False
        if "type" in chatInfo:
            if chatInfo["type"] == "private":
                key = "private:%s" % chatInfo["recipient"]
            elif chatInfo["type"] == "channel":
                if "channel" in chatInfo:
                    key = "channel:%s" % chatInfo["channel"]
                else:
                    key = "channel:%s" % self.currentChannel
        if key != None and key in self.lastChatTimestamps:
            lastTime = self.lastChatTimestamps[key]
            if lastTime != None:
                if lastTime >= time.time() - 2:
                    doThrottle = True

        # Send the message(s).
        chats = []
        for message in messages:
            if doThrottle:
                time.sleep(2)
            r = SendChatRequest(self.session, message)
            data = r.doRequest()
            tmpChats = data["chatMessages"]
            for chat in tmpChats:
                chats.append(chat)
            doThrottle = True

        if key != None:
            self.lastChatTimestamps[key] = time.time()

        for chat in chats:
            if 'listen' in chat['type'] or 'channel' in chat['type']:
                self.currentChannel = chat['currentChannel']

        return chats
