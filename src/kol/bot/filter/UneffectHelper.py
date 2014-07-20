"""
This module implements a FilterManager filter for removing unwanted effects. It
lets players send kmails or chat PMs telling the bot to remove any effect with
an SGEEA.
"""

import kol.Error as Error
from kol.bot import BotUtils
from kol.database import ItemDatabase
from kol.manager import FilterManager
from kol.request.UneffectRequest import UneffectRequest
from kol.util import Report

import re

UNEFFECT_PATTERN = re.compile(r'uneffect ([0-9]+)', re.IGNORECASE)

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "botProcessKmail":
        returnCode = botProcessKmail(context, **kwargs)
    elif eventName == "botProcessChat":
        returnCode = botProcessChat(context, **kwargs)
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
            raise Error.Error("You must specify the ID of the effect to remove.", Error.BOT_REQUEST)
        try:
            effectId = int(arr[1])
        except ValueError:
            raise Error.Error("Unable to remove effect. Invalid effect ID.", Error.BOT_REQUEST)

        # Ensure the user sent a SGEEA.
        if len(items) != 1:
            raise Error.Error("Please include just a SGEEA in your kmail.", Error.BOT_REQUEST)
        sgeea = ItemDatabase.getItemFromName("soft green echo eyedrop antidote")
        if items[0]["id"] != sgeea["id"] or items[0]["quantity"] != 1:
            raise Error.Error("Please include just a single SGEEA in your kmail.", Error.BOT_REQUEST)

        # Perform the request.
        m = {}
        m["userId"] = message["userId"]
        Report.info("bot", "Attempting to remove effect %s..." % effectId)
        r = UneffectRequest(bot.session, effectId)
        try:
            r.doRequest()
            m["text"] = "Effect successfully removed!"
        except Error.Error, inst:
            if inst.code == Error.EFFECT_NOT_FOUND:
                m["text"] = "I do not currently have that effect."
                m["items"] = items
            else:
                m["text"] = "Unable to remove effect for unknown reason."
                m["items"] = items

        bot.sendKmail(m)
        returnCode = FilterManager.FINISHED

    return returnCode

def botProcessChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    bot = kwargs["bot"]
    chat = kwargs["chat"]
    if chat["type"] == "private":
        match = UNEFFECT_PATTERN.search(chat["text"])
        if match:
            effectId = int(match.group(1))
            r = UneffectRequest(bot.session, effectId)
            try:
                r.doRequest()
                resp = "Effect successfully removed!"
            except Error.Error, inst:
                if inst.code == Error.EFFECT_NOT_FOUND:
                    resp = "I do not currently have that effect."
                elif inst.code == Error.ITEM_NOT_FOUND:
                    resp = "I do not have any SGEEAs. Would you be kind enough to send me some?"
                else:
                    resp = "Unable to remove effect for unknown reason."

            bot.sendChatMessage("/w %s %s" % (chat["userId"], resp))
            returnCode = FilterManager.FINISHED

    return returnCode
