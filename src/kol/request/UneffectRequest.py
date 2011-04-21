import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report

class UneffectRequest(GenericRequest):
    "Uses a soft green echo eyedrop antidote to remove any effect."

    def __init__(self, session, effectId):
        super(UneffectRequest, self).__init__(session)
        self.url = session.serverURL + "uneffect.php"
        self.requestData["using"] = "Yep."
        self.requestData["pwd"] = session.pwd
        self.requestData["whicheffect"] = effectId

    def parseResponse(self):
        # Check for errors.
        effectRemovedPattern = PatternManager.getOrCompilePattern('effectRemoved')
        if effectRemovedPattern.search(self.responseText):
            return

        youDontHaveThatEffectPattern = PatternManager.getOrCompilePattern('youDontHaveThatEffect')
        if youDontHaveThatEffectPattern.search(self.responseText):
            raise Error.Error("Unable to remove effect. The user does not have that effect.", Error.EFFECT_NOT_FOUND)

        youDontHaveSGEEAPattern = PatternManager.getOrCompilePattern('youDontHaveSGEEA')
        if youDontHaveSGEEAPattern.search(self.responseText):
            raise Error.Error("Unable to remove effect. You do not have a soft green echo eyedrop antidote.", Error.ITEM_NOT_FOUND)

        Report.error("request", "Unknown error occurred when trying to remove an effect")
        Report.error("request", self.responseText)
        raise Error.Error("Unknown error occurred when trying to remove an effect.", Error.REQUEST_FATAL)
