#!/usr/bin/python

import datetime
from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase

# There will be nested dictionaries
# cardLibrary's keys will be usernames
# cardLibrary[username]'s keys will be card names, and their
# values will be cards. 

def cardListToDict(cl):
    cardLib = {}
    for c in cl:
        name = c.name
        cardLib[name] = c
    return cardLib

    

# Class for a date range
# Lets you check if something is actually inside of the two dates. 
class dateRange():
    
    # Takes a start and end date as its arguments. 
    # They must already be datetime.datetime objects. 
    def __init__(self, start, end):
        if type(start) == type(end) == datetime.datetime:
            self.start = start
            self.end = end
        else:
            raise ValueError('start and end must be datetime.datetime objects')

    def isInRange(self, date):
        return (self.start <= date <= self.end)

# Convert "yyyy-mm-dd" format dates to datetime.datetime objects
def dateStrToObj(dateStr):
    return datetime.datetime.strptime(dateStr, '%Y-%m-%d')

# Convert a tuple of two "yyyy-mm-dd" format dates to a tuple of
# two datetime.datetime objects
def rangeStrToObj(range):
    start = dateStrToObj(range[0])
    end = dateStrToObj(range[1])
    return dateRange(start, end)

# A card that displays always, independent of the date
class card():
    def __init__(self, name, comment = ''):
        self.name = name
        self.comment = comment

    def shouldBeDisplayed(self, date):
        return True

    def __bool__(self):
        return True


# A card that displays conditionally based on the date
class cardCD(card):
    # Date range(s) specified as ('yyyy-mm-dd', 'yyyy-mm-dd') denoting
    # the start and end dates of when that card should be displayed
    # It can either be a single ranges as a tuple, or multiple as a list
    def __init__(self, name, ranges = [], comment = ''):
        self.name = name
        self.comment = comment
        if type(ranges) == tuple:
            self.ranges = [rangeStrToObj(ranges)]

        elif type(ranges) == list:
            self.ranges = []
            for r in ranges:
                self.ranges.append(rangeStrToObj(r))

        else:
            raise ValueError('Expected list or tuple for "ranges" argument.')
                


    def shouldBeDisplayed(self, date):
        return self.isInRange(date)

    def isInRange(self, date):
        for r in self.ranges:
            if r.isInRange(date):
                return True
        return False

# A card that should never display
class cardN(card):
    def shouldBeDisplayed(self, date):
        return False
    



