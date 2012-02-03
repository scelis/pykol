from GenericRequest import GenericRequest
from kol.util import ChatUtils

import time
import unicodedata
import urllib

class SendChatRequest(GenericRequest):
    def __init__(self, session, text):
        super(SendChatRequest, self).__init__(session)
        self.text = text.strip()
        self.url = session.serverURL + "submitnewchat.php?playerid=%s&pwd=%s" % (session.userId, session.pwd)
        self.url += "&%s" % urllib.urlencode({"graf":unicodedata.normalize('NFKD', self.text.decode('utf-8')).encode('ascii','ignore')})

    def parseResponse(self):
        # Parse the chat messages returned.
        self.responseData["chatMessages"] = ChatUtils.parseOutgoingChatMessages(self.responseText)
