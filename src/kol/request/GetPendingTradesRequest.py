from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.database import ItemDatabase

INCOMING = 1
OUTGOING = 2
INCOMING_RESPONSE = 3
OUTGOING_RESPONSE = 4

class GetPendingTradesRequest(GenericRequest):
    
    def __init__(self, session):
        super(GetPendingTradesRequest, self).__init__(session)
        self.url = session.serverURL + "makeoffer.php"
    
    def parseResponse(self):
        """
        Parse each different kind of trade. Each trade offer or offer and response is represented as a dictionary with following keys:
        
        tradeID:        The ID of the trade.
        tradeType:      The type of the trade - OUTGOING, INCOMING, etc.
        playerID:       The ID of the other player involved in this trade.
        playerName:     The name of the other player involved in this trade.
        incomingitems:  An array of items being offered to you in the format of a dictionary with keys itemID, quantity, and itemName.
        outgoingitems:  An array of items being offered to the other player in the format of a dictionary with keys itemID, quantity, and itemName.
        incomingmeat:   The amount of meat being offered by the other player.
        outgoingmeat:   The amount of meat being offered to the other player.
        message:        The message or note attached to the trade.
        """
        outgoingResponsePattern = PatternManager.getOrCompilePattern('tradePendingResponseOutgoing')
        incomingResponsePattern = PatternManager.getOrCompilePattern('tradePendingResponseIncoming')
        outgoingPattern = PatternManager.getOrCompilePattern('tradePendingOfferOutgoing')
        incomingPattern = PatternManager.getOrCompilePattern('tradePendingOfferIncoming')
        messagePattern = PatternManager.getOrCompilePattern('tradeMessage')
        itemPattern = PatternManager.getOrCompilePattern('tradeItem')
        
        tradeoffers = []
        
        iters = [incomingPattern.finditer(self.responseText), outgoingPattern.finditer(self.responseText), incomingResponsePattern.finditer(self.responseText), outgoingResponsePattern.finditer(self.responseText)]
        for matchset in iters:
            for trade in matchset:
                tradeType = iters.index(matchset) + 1
                tradeID = trade.group('tradeid')
                playerID = trade.group('playerid')
                playerName = trade.group('playername')
                try:
                    incomingitems = trade.group('incomingitems')#To be formatted later
                except:
                    incomingitems = None
                try:
                    outgoingitems = trade.group('outgoingitems')#To be formatted later
                except:
                    outgoingitems = None
                try:
                    incomingmeat = int(trade.group('incomingmeat'))
                except:
                    incomingmeat = None
                try:
                    outgoingmeat = int(trade.group('outgoingmeat'))
                except:
                    outgoingmeat = None
                message = trade.group('message')#To be formatted later
                iitems = []
                if incomingitems != None:
                    for item in itemPattern.finditer(incomingitems):
                        iitems.append({
                            'itemID': item.group(ItemDatabase.getItemFromDescId(item.group('itemdescid'))),
                            'itemName': item.group(item.group('itemname')),
                            'quantity': item.group('quantity')
                        })
                oitems = []
                if outgoingitems != None:
                    for item in itemPattern.finditer(outgoingitems):
                        oitems.append({
                            'itemID': item.group(ItemDatabase.getItemFromDescId(item.group('itemdescid'))),
                            'itemName': item.group(item.group('itemname')),
                            'quantity': item.group('quantity')
                        })
                try:
                    message = messagePattern.search(message).group('message')
                except:
                    message = None
                tradeoffers.append({
                    'tradeID': tradeID,
                    'tradeType': tradeType,
                    'playerID': playerID,
                    'playerName': playerName,
                    'incomingitems': iitems,
                    'outgoingitems': oitems,
                    'incomingmeat': incomingmeat,
                    'outgoingmeat': outgoingmeat,
                    'message': message,
                })
        self.responseData['trades'] = tradeoffers