import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager

class CafeMenuRequest(GenericRequest):
    "Check the current menu at a cafe."

    CHEZ_SNOOTEE ='1'
    MICROBREWERY = '2'
    HELLS_KITCHEN = '3'

    def __init__(self, session, cafe):
        super(CafeMenuRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "cafe.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['cafeid'] = cafe

    def parseResponse(self):
        menuItemPattern = PatternManager.getOrCompilePattern('menuItem')
        cannotGoPattern = PatternManager.getOrCompilePattern('userShouldNotBeHere')

        if cannotGoPattern.search(self.responseText):
            raise Error.Error("You cannot reach that cafe.", Error.INVALID_LOCATION)

        items = []
        for match in menuItemPattern.finditer(self.responseText):
            descId = match.group(2)
            if descId.isdigit():
                descId = int(descId)
            item = ItemDatabase.getItemFromDescId(descId)
            items.append(item)

        if len(items) == 0:
            raise Error.Error("Retrieved an Empty Menu", Error.REQUEST_GENERIC)

        self.responseData["menu"] = items
