"""
The purpose of this class is to provide a one-stop-shop for getting and storing compiled
regular expression patterns. I have found that often patterns can be shared across different
request types, so it makes sense to have a central location to store them instead of storing
copies in each class.
"""

from kol.data import Patterns

import re

__compiledPatterns = {}

def getOrCompilePattern(patternId):
    """
    Returns a compiled regular expression pattern if it already exists. If it doesn't, this
    method will compile the regular expression and then store it so that it does not need
    to be compiled again.
    """
    if patternId in __compiledPatterns:
        return __compiledPatterns[patternId]

    if patternId in Patterns.patterns:
        pattern = Patterns.patterns[patternId]
        if type(pattern) == str:
            __compiledPatterns[patternId] = re.compile(pattern)
        elif type(pattern) == tuple:
            __compiledPatterns[patternId] = re.compile(pattern[0], pattern[1])
        else:
            raise TypeError("Unexpected type found for pattern '%s'" % patternId)
        return __compiledPatterns[patternId]

    raise KeyError("Pattern '%s' not found." % patternId)
