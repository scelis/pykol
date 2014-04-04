import re
from GenericRequest import GenericRequest
from kol.database import ItemDatabase

class ClanStashRequest(GenericRequest):
    "This class is used to get a list of items in the user's clan stash."

    def __init__(self, session, which=None):
        super(ClanStashRequest, self).__init__(session)
        self.url = session.serverURL + "clan_stash.php"
        self.requestData["pwd"] = session.pwd

    def parseResponse(self):
        items = []
        pattern = re.compile(r'<option value=(?P<val>\d*) descid=\d*>(?P<item>.*?)( \((?P<qty>\d*)\))?( \(-(?P<cost>\d*)\))?</option>')
        handy_list = pattern.findall(self.responseText)
        for item in handy_list:
            temp = {}
            temp["id"] = int(item[0])
            temp["name"] = item[1]
            if item[3] == '':
                temp["quantity"] = 1
            else:
                temp["quantity"] = int(item[3])
            temp["cost"] = item[5]
            #if item[3] == '':
            #    temp["cost"] = 0
            #else:
            #    temp["cost"] = int(item[3][2:-1])
            items.append(temp)
        self.responseData["items"] = items
