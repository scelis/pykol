"""
This module implements a FilterManager filter to allow bots to broadcast their /clan chat
to other bots being run in this process. Users may prefix their chats with 'PRIVATE:' to
tell the bot to not broadcast that particular message. In addition, users with sufficient
privileges may tell the bot to stop or start broadcasting at any time by sending a private
message with the text 'squelch' or 'unsquelch'. Finally, players may also send a private
message with the text 'who' to see which players are in the same channel as the bot.
"""

from kol.bot import BotManager
from kol.bot import BotUtils
from kol.manager import FilterManager
from kol.util import DataUtils
from kol.util import Report

def doFilter(eventName, context, **kwargs):
	returnCode = FilterManager.CONTINUE
	if eventName == "botProcessChat":
		returnCode = botProcessChat(context, **kwargs)
	return returnCode

def botProcessChat(context, **kwargs):
	returnCode = FilterManager.CONTINUE
	chat = kwargs["chat"]
	
	if chat["type"] in ["normal", "emote"] and chat["channel"] == "clan":
		returnCode = handleClanChat(context, **kwargs)
	elif chat["type"] in ["private"]:
		returnCode = handlePrivateChat(context, **kwargs)
		
	return returnCode

def handleClanChat(context, **kwargs):
	chat = kwargs["chat"]
	bot = kwargs["bot"]
	globalState = bot.states["global"]
	
	# Do nothing if the bot is squelched.
	if DataUtils.getBoolean(globalState, "isSquelched", False):
		return FilterManager.CONTINUE
	
	# Do nothing if the text is prefixed by PRIVATE:
	lowerText = chat["text"].lower()
	if lowerText.find("private:") == 0:
		return FilterManager.CONTINUE
	
	# Do nothing for broadcasted messages.
	if chat["userName"] == "System Message":
		return FilterManager.CONTINUE
	
	# Construct the message to send to the other bots.
	msg = None
	if chat["type"] == "normal":
		msg = "/clan [%s] %s" % (chat["userName"], chat["text"])
	elif chat["type"] == "emote":
		msg = "/clan <%s %s>" % (chat["userName"], chat["text"])
	
	# Send the message to the other bots.
	if msg != None:
		thisBot = kwargs["bot"]
		for bot in BotManager._bots:
			if bot.id != thisBot.id:
				bot.sendChatMessage(msg)
	
	return FilterManager.CONTINUE

def handlePrivateChat(context, **kwargs):
	returnCode = FilterManager.CONTINUE
	chat = kwargs["chat"]
	bot = kwargs["bot"]
	globalState = bot.states["global"]
	
	if chat["text"] == "squelch":
		if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
			globalState["isSquelched"] = True
			bot.writeState("global")
			bot.sendChatMessage("No longer broadcasting /clan to the other clan channels.")
		else:
			bot.sendChatMessage("You do not have permission to perform this action.")
		returnCode = FilterManager.FINISHED
	elif chat["text"] == "unsquelch":
		if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
			globalState["isSquelched"] = False
			bot.writeState("global")
			bot.sendChatMessage("Now broadcasting /clan to the other clan channels.")
		else:
			bot.sendChatMessage("You do not have permission to perform this action.")
		returnCode = FilterManager.FINISHED
	elif chat["text"] == "squelchall":
		if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
			for aBot in BotManager._bots:
				aBot.states["global"]["isSquelched"] = True
				aBot.writeState("global")
				aBot.sendChatMessage("All bots have been squelched.")
		else:
			bot.sendChatMessage("You do not have permission to perform this action.")
		returnCode = FilterManager.FINISHED
	elif chat["text"] == "unsquelchall":
		if BotUtils.canUserPerformAction(chat["userId"], "squelch", bot):
			for aBot in BotManager._bots:
				aBot.states["global"]["isSquelched"] = False
				aBot.writeState("global")
				aBot.sendChatMessage("All bots have been unsquelched.")
		else:
			bot.sendChatMessage("You do not have permission to perform this action.")
		returnCode = FilterManager.FINISHED
	elif chat["text"] == "who":
		response = bot.sendChatMessage("/who")
		whoChat = response[0]
		str = ""
		for user in whoChat["users"]:
			if user["userName"] != bot.id:
				if len(str) > 0:
					str += ", "
				str += user["userName"]
		if len(str) > 0:
			bot.sendChatMessage("/w %s %s" % (chat["userId"], str))
		else:
			bot.sendChatMessage("/w %s There is no one else in my clan channel." % chat["userId"])
		returnCode = FilterManager.FINISHED
	
	return returnCode
