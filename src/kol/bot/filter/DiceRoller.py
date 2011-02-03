"""
This module implements a FilterManager filter to provide basic dice-rolling
functionality.
"""

from kol.manager import FilterManager
from kol.manager import PatternManager
from kol.util import Report

import random
import re

DICE_ROLL_PATTERN = re.compile(r'roll ([0-9]+)d([0-9]+)', re.IGNORECASE)

def doFilter(eventName, context, **kwargs):
    returnCode = FilterManager.CONTINUE
    if eventName == "botProcessChat":
        returnCode = botProcessChat(context, **kwargs)
    return returnCode

def botProcessChat(context, **kwargs):
    returnCode = FilterManager.CONTINUE
    bot = kwargs["bot"]
    chat = kwargs["chat"]
    if chat["type"] in ["private"]:
        match = DICE_ROLL_PATTERN.search(chat["text"])
        if match:
            # Get the number of dice and the number of sides on each die.
            numDice = int(match.group(1))
            numSides = int(match.group(2))
            if numDice > 10:
                numDice = 10
            elif numDice <= 0:
                numDice = 1
            if numSides <= 0:
                numSides = 1

            # Roll the dice.
            result = []
            for i in range(numDice):
                result.append(random.randint(1, numSides))

            # Print out the information.
            msg = "Rolling %sd%s for %s gives: " % (numDice, numSides, chat["userName"])
            i = 0
            for r in result:
                if i > 0:
                    msg += ", "
                msg += str(r)
                i += 1
            bot.sendChatMessage(msg)

            returnCode = FilterManager.FINISHED

    return returnCode
