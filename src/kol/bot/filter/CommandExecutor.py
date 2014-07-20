"""
This module implements a FilterManager filter that allows users with sufficient
privileges to execute arbitrary chat commands.
"""

from kol.bot import BotManager
from kol.bot import BotUtils
from kol.manager import FilterManager
from kol.util import Report

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "botProcessChat":
        returnCode = botProcessChat(context, **kwargs)
    return returnCode

def botProcessChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    chat = kwargs["chat"]
    
    if chat["type"] == "private":
        if BotUtils.canUserPerformAction(chat["userId"], "execute", kwargs["bot"]):
            doAction = False
            executeAll = False
            wordList = chat["text"].split()
            if len(wordList) > 0:
                if wordList[0].lower() == "execute":
                    doAction = True
                elif wordList[0].lower() == "executeall":
                    doAction = True
                    executeAll = True

            if doAction:
                returnCode = FilterManager.FINISHED
                del wordList[0]
                command = " ".join(wordList)

                if executeAll:
                    for bot in BotManager._bots:
                        if bot.session != None and bot.session.isConnected and hasattr(bot.session, "chatManager"):
                            try:
                                bot.sendChatMessage(command)
                            except AttributeError, inst:
                                Report.error("chat", "Could not execute command: %s" % command, inst)
                else:
                    kwargs["bot"].sendChatMessage(command)

    return returnCode
