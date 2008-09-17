from kol.manager import FilterManager

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
