from GenericRequest import GenericRequest
from kol.Error import RequestError
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import StringUtils

from datetime import datetime

class GetMessagesRequest(GenericRequest):
    """
    This class is used to get a list of kmails from the server.
    """
    
    def __init__(self, session, box="Inbox", pageNumber=None, messagesPerPage=None, oldestFirst=None):
        """
        Initializes the GetMessagesRequest object. Due to a bug in KoL,
        it is highly recommended that you do not specify more than one
        of pageNumber, messagesPerPage, and oldestFirst in the same
        request. Doing so can cause the server to take up to 5 minutes
        to respond to your request. For now, if you want to specify two
        or three of these parameters, you should specify one at a time
        and make multiple requests. KoL is nice enough to remember the
        values you last used for both messagesPerPage and oldestFirst.
        """
        
        super(GetMessagesRequest, self).__init__(session)
        self.url = session.serverURL + "messages.php?box=%s" % box
        
        if pageNumber and pageNumber > 1:
            self.url += "&begin=%s" % pageNumber
        
        if messagesPerPage:
            if messagesPerPage not in [10,20,50,100]:
                raise RequestError("%s is not a valid number of messages to request per page. Please specify 10, 20, 50, or 100." % messagesPerPage)
            self.url += "&per_page=%s" % (messagesPerPage / 10)
        
        if oldestFirst == True:
            self.url += "&order=1"
        elif oldestFirst == False:
            self.url += "&order=0"
    
    def parseResponse(self):
        """
        Parses through the response and constructs an array of messages.
        Each message is represented as a dictionary with the following
        keys:
        
              id -- The integer identifier for the message.
          userId -- The ID of the user who sent or received this message.
        userName -- The name of the user who sent or received this message.
            date -- The date the message was sent as a datetime object.
            text -- The contents of the message.
           items -- An array of items attached to the message.
            meat -- The amount of meat sent with the message.
        """
        
        fullMessagePattern = PatternManager.getOrCompilePattern('fullMessage')
        whitespacePattern = PatternManager.getOrCompilePattern('whitespace')
        singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
        multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
        meatPattern = PatternManager.getOrCompilePattern('gainMeat')
        brickPattern = PatternManager.getOrCompilePattern('brickMessage')
        coffeePattern = PatternManager.getOrCompilePattern('coffeeMessage')
        candyHeartPattern = PatternManager.getOrCompilePattern('candyHeartMessage')
        
        messages = []
        
        for message in fullMessagePattern.finditer(self.responseText):
            messageId = int(message.group(1))
            userId = int(message.group(2))
            userName = message.group(3).strip()
            
            dateStr = message.group(4).strip()
            try:
                date = datetime.strptime(dateStr, "%A, %B %d, %Y, %I:%M%p")
            except ValueError:
                date = dateStr
            
            rawText = message.group(5).strip()
            index = rawText.find('<center')
            if index >= 0:
                text = rawText[:index].strip()
            else:
                text = rawText.strip()
                
            # Get rid of extraneous spaces, tabs, or new lines.
            text = text.replace("\r\n", "\n")
            text = whitespacePattern.sub(' ', text)
            text = text.replace("<br />\n", "\n")
            text = text.replace("<br/>\n", "\n")
            text = text.replace("<br>\n", "\n")
            text = text.replace("\n<br />", "\n")
            text = text.replace("\n<br/>", "\n")
            text = text.replace("\n<br>", "\n")
            text = text.replace("<br />", "\n")
            text = text.replace("<br/>", "\n")
            text = text.replace("<br>", "\n")
            text = text.strip()
            
            # KoL encodes all of the HTML entities in the message. Let's decode them to get the real text.
            text = StringUtils.htmlEntityDecode(text)
            
            m = {"id":messageId, "userId":userId, "userName":userName, "date":date, "text":text}
            
            # Find the items attached to the message.
            items = []
            for match in singleItemPattern.finditer(rawText):
                descId = int(match.group(1))
                item = ItemDatabase.getItemFromDescId(descId, self.session)
                item["quantity"] = 1
                items.append(item)
            for match in multiItemPattern.finditer(rawText):
                descId = int(match.group(1))
                quantity = int(match.group(2).replace(',', ''))
                item = ItemDatabase.getItemFromDescId(descId, self.session)
                item["quantity"] = quantity
                items.append(item)
            m["items"] = items
            
            # Find how much meat was attached to the message.
            meat = 0
            meatMatch = meatPattern.search(rawText)
            if meatMatch:
                meat = int(meatMatch.group(1).replace(',', ''))
            m["meat"] = meat
            
            # Handle special messages.
            if brickPattern.search(rawText):
                m["messageType"] = "brick"
            elif coffeePattern.search(rawText):
                m["messageType"] = "coffeeCup"
            elif candyHeartPattern.search(rawText):
                m["messageType"] = "candyHeart"
            else:
                m["messageType"] = "normal"
            
            messages.append(m)
                    
        self.responseData["kmails"] = messages
