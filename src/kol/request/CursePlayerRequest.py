import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class CursePlayerRequest(GenericRequest):
    def __init__(self, session, targetPlayerNameOrId, itemId):
        super(CursePlayerRequest, self).__init__(session)
        self.url = session.serverURL + "curse.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "use"
        self.requestData["whichitem"] = itemId
        self.requestData["targetplayer"] = targetPlayerNameOrId
        self.curseItemId = itemId

    def parseResponse(self):
        if len(self.responseText) < 10:
            raise Error.Error("You can't curse with that item.", Error.WRONG_KIND_OF_ITEM)

        dontHaveThatItemPattern = PatternManager.getOrCompilePattern('dontHaveThatItem')
        if dontHaveThatItemPattern.search(self.responseText):
            raise Error.Error("You don't have that item.", Error.ITEM_NOT_FOUND)

        playerNotFoundPattern = PatternManager.getOrCompilePattern('cantCursePlayerNotFound')
        if playerNotFoundPattern.search(self.responseText):
            raise Error.Error("That player could not be found.", Error.USER_NOT_FOUND)

        if self.curseItemId == 4939:
            cantFireAtSelfPattern = PatternManager.getOrCompilePattern('cantFireArrowAtSelf')
            if cantFireAtSelfPattern.search(self.responseText):
                raise Error.Error("You can't fire an arrow at yourself.", Error.INVALID_USER)

            cantFireHardcoreRonin = PatternManager.getOrCompilePattern('cantFireArrowAtHardcoreRonin')
            if cantFireHardcoreRonin.search(self.responseText):
                raise Error.Error("You can't fire an arrow at a person in hardcore or ronin.", Error.USER_IN_HARDCORE_RONIN)

            alreadyHitPattern = PatternManager.getOrCompilePattern('userAlreadyHitWithArrow')
            if alreadyHitPattern.search(self.responseText):
                raise Error.Error("That person has already been arrowed today.", Error.ALREADY_COMPLETED)

            successPattern = PatternManager.getOrCompilePattern('fireArrowSuccess')
            if not successPattern.search(self.responseText):
                print self.responseText
                raise Error.Error("Unknown error.", Error.REQUEST_GENERIC)
