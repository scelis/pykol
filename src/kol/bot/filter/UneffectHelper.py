"""
This module implements a FilterManager filter for removing unwanted effects.
"""

from kol.Error import ParseMessageError, DontHaveEffectError, NotEnoughItemsError
from kol.bot import BotUtils
from kol.database import ItemDatabase
from kol.manager import FilterManager
from kol.request.UneffectRequest import UneffectRequest

def doFilter(eventName, context, **kwargs):
	returnCode = FilterManager.CONTINUE
	if eventName == "botProcessKmail":
		returnCode = botProcessKmail(context, **kwargs)
	return returnCode

def botProcessKmail(context, **kwargs):
	returnCode = FilterManager.CONTINUE
	message = kwargs["kmail"]
	bot = kwargs["bot"]
	cmd = BotUtils.getKmailCommand(message)
	
	if cmd == "uneffect":
		arr = message["text"].split()
		items = message["items"]
		
		# Get the effect ID.
		if len(arr) < 2:
			raise ParseMessageError("You must specify the ID of the effect to remove.")
		try:
			effectId = int(arr[1])
		except ValueError:
			raise ParseMessageError("Unable to remove effect. Invalid effect ID.")
		
		# Ensure the user sent a SGEEA.
		if len(items) != 1:
			raise ParseMessageError("Please include just a SGEEA in your kmail.")
		sgeea = ItemDatabase.getItemFromName("soft green echo eyedrop antidote")
		if items[0]["id"] != sgeea["id"] or items[0]["quantity"] != 1:
			raise ParseMessageError("Please include just a single SGEEA in your kmail.")
		
		# Perform the request.
		m = {}
		m["userId"] = message["userId"]
		r = UneffectRequest(bot.session, effectId)
		try:
			r.doRequest()
			m["text"] = "Effect successfully removed!"
		except DontHaveEffectError, inst:
			m["text"] = "I do not currently have that effect."
			m["items"] = items
		except Error, inst:
			m["text"] = "Unable to remove effect for unknown reason."
			m["items"] = items
		
		bot.sendKmail(m)
		returnCode = FilterManager.FINISHED
			
	return returnCode
