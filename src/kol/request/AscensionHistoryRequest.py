from GenericRequest import GenericRequest
from kol.manager import PatternManager
from datetime import timedelta, datetime

class AscensionHistoryRequest(GenericRequest):
    def __init__(self, session, playerId, preNS13=False):
        super(AscensionHistoryRequest, self).__init__(session)
        self.url = session.serverURL + "ascensionhistory.php?back=other&who=%s" % playerId
        if preNS13:
            self.url += "&prens13=1"
    
    def parseResponse(self):
        """
        Parses through the response and constructs an array of ascensions.
        Each ascension is represented as a dictionary with the following
        keys:

              id -- The ascension #.
           start -- The start date of the ascension (as datetime).
             end -- The end date of the ascension (as datetime).
           level -- The level at which the user ascended.
           class -- The class of the user during the ascension
            sign -- The sign of the user during the ascension
           turns -- The number of turns the ascension lasted
            days -- The number of days the ascension lasted
        familiar -- The most used familiar this ascension
        famUsage -- The use percentage of the most used familiar
            type -- The type of ascension (normal, hardcore, casual, BM)
            path -- The path of the ascension (teet, booze, oxy)
        """
        
        fullAscensionPattern = PatternManager.getOrCompilePattern('fullAscension')
        famPattern = PatternManager.getOrCompilePattern('familiarAscension')
        
        ascensions = []
        
        stripText = self.responseText.replace("&nbsp;", "")
        for ascension in fullAscensionPattern.finditer(stripText):
            ascNumber = ascension.group(1)
            ascDate = ascension.group(2)
            ascLevel = int(ascension.group(3))
            ascClass = ascension.group(4).strip()
            ascSign = ascension.group(5).strip()
            ascTurns = int(ascension.group(6).replace(',',''))
            ascDays = int(ascension.group(7).replace(',',''))
            ascFamiliarData = ascension.group(8)
            ascType = ascension.group(10)
            ascPath = ascension.group(12)
            
            try:
                ascEnd = datetime.strptime(ascDate, "%m/%d/%y")
            except ValueError:
                ascEnd = dateStr
        
            runlength = timedelta(ascDays - 1)
            ascStart = ascEnd - runlength
    
            if ascFamiliarData == "No Data":
                ascFamiliar = "None"
                ascFamUsage = 0
            else:
                for match in famPattern.finditer(ascFamiliarData):
                    ascFamiliar = match.group(1).strip()
                    ascFamUsage = match.group(2)
    
            if ascType == "Hardcore" and ascPath == "Bad Moon":
                ascType = "Bad Moon"
                ascPath = "None"
        
            asc = {"id":ascNumber, "start":ascStart, "end":ascEnd, "level":ascLevel, "class":ascClass, "sign":ascSign, "turns":ascTurns, "days":ascDays, "familiar":ascFamiliar, "famUsage":ascFamUsage, "type":ascType, "path":ascPath}
            
            ascensions.append(asc)
        
        self.responseData["ascensions"] = ascensions
