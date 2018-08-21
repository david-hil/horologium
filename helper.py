import math

def parseTime(secspassed):
    hours = math.trunc(secspassed/3600)
    secspassed -= 3600*hours
    minutes = math.trunc(secspassed/60)
    secspassed -= 60 * minutes
    seconds = math.trunc(secspassed)
    output = " {}h {}:{}min".format(hours, minutes if minutes > 9 else "0{}".format(minutes), seconds if seconds > 9 else "0{}".format(seconds))
    return output

def parseTask(task):
    return "{} {}".format(task[2] if task[2] else "task", "[{}]".format(task[1]) if task[1] else "")