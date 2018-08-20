import math

def parseTime(timepassed):
    hours = math.trunc(timepassed/3600)
    timepassed -= 3600*hours
    minutes = math.trunc(timepassed/60)
    timepassed -= 60 * minutes
    seconds = math.trunc(timepassed)
    output = " {}h {}:{}min".format(hours, minutes if minutes > 9 else "0{}".format(minutes), seconds if seconds > 9 else "0{}".format(seconds))
    return output
