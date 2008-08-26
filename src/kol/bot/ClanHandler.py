from kol.manager import FilterManager
from kol.request.BootClanMemberRequest import BootClanMemberRequest

def doFilter(eventName, context, **kwargs):
	returnCode = FilterManager.CONTINUE
	if eventName == "botProcessChat":
		returnCode = botProcessChat(context, **kwargs)
	return returnCode

def botProcessChat(context, **kwargs):
	returnCode = FilterManager.CONTINUE
	chat = kwargs["chat"]
	bot = kwargs["bot"]
	return returnCode
