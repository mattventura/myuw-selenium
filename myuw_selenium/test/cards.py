#!/usr/bin/python

from myuw_selenium.test.cardclasses import card, cardCD, cardN
from cardclasses import *


# Specfify dates to test here
# In addition, days immediately before and after a card is supposed 
# to show or hide will automatically be added. 
# Dates before minDate will not automatically be added. 
minDate = '2013-01-07'
testDates = {}
testDates['javerage'] = set([
    '2013-01-07', # First day of winter quarter
    '2013-01-10', # Spring future quarter card should move to bottom
    '2013-01-15', # One week into quarter, plus one day
    '2013-02-14', # Day before first day of P1 reg
    '2013-02-15', # First day of P1 reg
    '2013-03-15', # Last day of classes for winter 2013
    '2013-03-16', # Finals begin, winter 2013 
    '2013-03-21', # Last day of finals
    '2013-03-22', # Spring break begins
    '2013-03-23', # Day after spring break begins
    '2013-03-25', # Day before grade submission deadline
    '2013-03-26', # Grade submission deadline
])


# Both start and end dates are inclusive
cardList = {}
cardList['javerage'] = [
    card('HFSCard'),
    card('TuitionCard'),
    card('LibraryCard'),
    card('AcademicCard'),
    card('CourseCard'),

    cardCD('VisualScheduleCard', ('2013-01-07', '2013-03-15')),
    cardCD('TextbookCard', ('2013-01-07', '2013-01-13')),
    cardCD('GradeCard', ('2013-03-16', '2013-03-26')),
    cardCD('FinalExamCard', ('2013-03-16', '2013-03-21')),
    cardCD('FutureQuarterCardA', ('2013-01-07', '2013-03-26')),
    # This card has "seen"-dependent logic, so it never actually appears at the 
    # bottom for our tests
    #card('FutureQuarterCard1', ('2013-03-12', '2013-03-27')),
    cardN('FutureQuarterCard1'),

    cardN('RegStatusCard'), 
    cardN('SummerRegStatusCardA'),
    cardN('SummerRegStatusCard1'),
    cardN('EventsCard'),

]

cardList['none'] = []

# Convert lists to libraries (keys are card name, values are card object)
cardLibrary = {}
# This uses testDates instead of cardList so that we don't do unnecessary work
# for users that we aren't actually going to test. 
for userName in testDates:
    cardLibrary[userName] = cardListToDict(cardList[userName])

# Automatically add dates
for userName in testDates:
    cl = cardList[userName]
    for card in cl:
        if hasattr(card, 'testDates'):
            for d in card.testDates:
                if d >= minDate:
                    testDates[userName].add(d)

