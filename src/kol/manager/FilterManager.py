"""
This module provides a standard way of registering and executing filter hooks.
"""

# A mapping from eventName to an array of filters.
__filters = {}

# Return codes that can be set by filters.
ABORT = 0
CONTINUE = 1
FINISHED = 2

def registerFilterForEvent(filter, eventName, loadOrder=10):
    """
    Registers a filter for a particular event. The loadOrder determines which order the filters
    are executed in when more than one filter is registered for a single event. The filters
    with the lowest loadOrder will be executed first.
    """
    if eventName in __filters:
        filtersForEvent = __filters[eventName]
        i = 0
        while i < len(filtersForEvent):
            if loadOrder >= filtersForEvent[i][1]:
                i += 1
            else:
                break

        filtersForEvent.insert(i, (filter, loadOrder))
    else:
        __filters[eventName] = [(filter, loadOrder)]

def executeFiltersForEvent(eventName, context=None, **kwargs):
    """
    Iterates through all filters registered for this particular event and executes then in
    order. A context is passed into each filter and then returned to allow filters to
    communicate with one another as well as with the original caller. We allow filters
    to end the execution chain early by returning FilterManager.ABORT or FilterManager.FINISHED.
    """
    if context == None:
        context = {}

    index = eventName.find(':')
    if index < 0:
        realEventName = eventName
    else:
        realEventName = eventName[:index]

    returnCode = CONTINUE
    keepGoing = True
    while keepGoing:
        if eventName in __filters:
            for filter in __filters[eventName]:
                returnCode = filter[0].doFilter(realEventName, context, **kwargs)
                if returnCode != CONTINUE:
                    keepGoing = False
                    break

        if eventName == realEventName:
            keepGoing = False
        else:
            index = eventName.rfind(':')
            if index >= 0:
                eventName = eventName[:index]

    return returnCode
