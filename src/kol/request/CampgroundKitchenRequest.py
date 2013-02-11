import kol.Error as Error
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.request.GenericRequest import GenericRequest

class CampgroundKitchenRequest(GenericRequest):
    "Checks state of the kitchen. (Did you wash the dishes?)"

    def __init__(self, session):
        super(CampgroundKitchenRequest, self).__init__(session)
        self.url = session.serverURL + "campground.php"
        self.requestData['action'] = 'inspectkitchen'
        self.requestData['pwd'] = session.pwd

    def parseResponse(self):
        hasOvenPattern = PatternManager.getOrCompilePattern('campgroundHasOven')
        hasRangePattern = PatternManager.getOrCompilePattern('campgroundHasRange')
        hasChefPattern = PatternManager.getOrCompilePattern('campgroundHasChef')
        hasShakerPattern = PatternManager.getOrCompilePattern('campgroundHasShaker')
        hasKitPattern = PatternManager.getOrCompilePattern('campgroundHasKit')
        hasBartenderPattern = PatternManager.getOrCompilePattern('campgroundHasBartender')
        hasMatPattern = PatternManager.getOrCompilePattern('campgroundHasMat')

        if hasOvenPattern.search(self.responseText):
            self.responseData["hasOven"] = 1

        if hasRangePattern.search(self.responseText):
            self.responseData["hasOven"] = 1
            self.responseData["hasRange"] = 1

        if hasChefPattern.search(self.responseText):
            self.responseData["hasChef"] = 1

        if hasShakerPattern.search(self.responseText):
            self.responseData["hasShaker"] = 1

        if hasKitPattern.search(self.responseText):
            self.responseData["hasShaker"] = 1
            self.responseData["hasCocktailKit"] = 1

        if hasBartenderPattern.search(self.responseText):
            self.responseData["hasBartender"] = 1

        if hasMatPattern.search(self.responseText):
            self.responseData["hasSushiMat"] = 1

