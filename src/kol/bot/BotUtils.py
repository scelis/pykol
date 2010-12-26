"""
This module is where basic utility methods used by bots can be placed.
"""

def getKmailCommand(kmail):
    wordList = kmail["text"].split()
    if len(wordList) > 0:
        return wordList[0].lower()
    return ""

def canUserPerformAction(userId, action, bot, default=False):
    ret = default
    if "actionPermissions" in bot.params and "userPermissions" in bot.params:
        if action in bot.params["actionPermissions"] and userId in bot.params["userPermissions"]:
            userPerms = bot.params["userPermissions"][userId]
            actionPerms = bot.params["actionPermissions"][action]
            if userPerms >= actionPerms:
                ret = True
    return ret
