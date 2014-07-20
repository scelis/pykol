import os
import threading
import time
import traceback

FATAL = 100
ALERT = 200
ERROR = 300
WARNING = 400
INFO = 500
TRACE = 600
DEBUG = 700

__outputSections = ["*"]
__outputLevel = TRACE
__logs = []
__logCurrentDate = None
__includeThreadName = False

def addOutputSection(sectionName):
    __outputSections.append(sectionName)

def removeOutputSection(sectionName):
    if sectionName in __outputSections:
        __outputSections.remove(sectionName)

def setOutputSections(arr):
    global __outputSections
    __outputSections = arr

def setOutputLevel(level):
    global __outputLevel
    __outputLevel = level

def setIncludeThreadName(includeThreadName):
    global __includeThreadName
    __includeThreadName = includeThreadName

def registerLog(directory, fileName, sections=["*"], level=INFO):
    log = {"fileName" : fileName, "sections" : sections, "level" : level}

    # If the directory doesn't exist, let's create it.
    if directory != None:
        log["directory"] = directory
        if not os.path.exists(directory):
            os.mkdir(directory)

    __logs.append(log)

def report(section, level, message, exception=None):
    global __logCurrentDate

    # Do we need to roll the logs over?
    currentDate = time.strftime("%Y-%m-%d")
    if currentDate != __logCurrentDate:
        for log in __logs:
            if "file" in log:
                log["file"].close()
                del log["file"]
        __logCurrentDate = currentDate

    # Should this message be printed?
    doPrint = False
    if ("*" in __outputSections or section in __outputSections) and level <= __outputLevel:
        doPrint = True

    # Should this message be logged?
    logs = []
    for log in __logs:
        s = log["sections"]
        if ("*" in s or section in s) and level <= log["level"]:
            logs.append(log)

    if doPrint or len(logs) > 0:
        # Create the full message string.
        fullMessage = None
        dateTimeStr = time.strftime("%Y-%m-%d %H:%M:%S")
        if __includeThreadName:
            threadName = threading.currentThread().getName()
            if threadName != "MainThread":
                fullMessage = "%s -- [%s] %s" % (dateTimeStr, threadName, message)
        if fullMessage == None:
            fullMessage = "%s -- %s" % (dateTimeStr, message)

        # Print the message.
        if doPrint:
            print fullMessage
            if exception != None:
                print traceback.format_exc()

        # Log the message.
        if len(logs) > 0:
            currentDate = time.strftime("%Y-%m-%d")
            for log in logs:
                if "file" not in log:
                    if "directory" in log:
                        filePath = os.path.join(log["directory"], log["fileName"] + '.' + currentDate)
                    else:
                        filePath = log["fileName"] + '.' + currentDate
                    log["file"] = open(filePath, 'a')

                log["file"].write("%s\n" % fullMessage)
                if exception != None:
                    log["file"].write(traceback.format_exc())
                log["file"].flush()

def fatal(section, message, exception=None):
    report(section, FATAL, message, exception)

def alert(section, message, exception=None):
    report(section, ALERT, message, exception)

def error(section, message, exception=None):
    report(section, ERROR, message, exception)

def warning(section, message, exception=None):
    report(section, WARNING, message, exception)

def info(section, message, exception=None):
    report(section, INFO, message, exception)

def trace(section, message, exception=None):
    report(section, TRACE, message, exception)

def debug(section, message, exception=None):
    report(section, DEBUG, message, exception)
