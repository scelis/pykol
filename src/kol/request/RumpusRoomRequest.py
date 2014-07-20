from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager

FURNITURE = {
    '1':{
        '0':'A Nail in the Wall',
        '1':'Girls of Loathing Calendar',
        '2':'Boys of Loathing Calendar',
        '3':'An Infuriating Painting',
        '4':'An Exotic Hanging Meat Orchid'
    },
    '2':{
        '0':'An Empty Bookshelf',
        '1':'A Collection of Arcane Tomes and Whatnot',
        '2':'A Collection of Sports Memorabilia',
        '3':'A Collection of Self-Help Books',
    },
    '3':{
        '0':'An Unused Outlet',
        '1':'A Soda Machine',
        '2':'A Jukebox',
        '3':'A Mr. Klaw "Skill" Crane Game',
    },
    '4':{
        '0':'An Empty Endtable',
        '1':'An Old-Timey Radio',
        '2':'A Potted Meat Bush',
        '3':'An Inspirational Desk Calendar',
    },
    '5':{
        '0':'A Threadbare Rug',
        '1':'A Wrestling Mat',
        '2':'A Tan-U-Lots Tanning Bed',
        '3':'A Comfy Sofa',
    },
    '6':{
        '0':'Some Empty Space',
    },
    '7':{
        '0':'A Bare Corner',
    },
    '8':{
        '0':'Doorway',
    },
    '9':{
        '0':'A Dusty Corner',
        '1':'A Hobo-Flex Workout System',
        '2':'A Snack Machine',
        '3':'A Potted Meat Tree',
    },
}

class RumpusRoomRequest(GenericRequest):
    "Determines what furniture is present in the rumpus room."
    def __init__(self, session):
        super(RumpusRoomRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php'

    def parseResponse(self):
        furnPresent = []
        rumpusRoomPattern = PatternManager.getOrCompilePattern('rumpusRoomFurniture')
        for match in rumpusRoomPattern.finditer(self.responseText):
            spot = match.group(1)
            furn = match.group(2)
            if furn != '0':
                furnPresent.append(FURNITURE[spot][furn])

        self.responseData["furniture"] = furnPresent
