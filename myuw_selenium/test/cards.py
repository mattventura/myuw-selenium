#!/usr/bin/python

from myuw_selenium.test.cardclasses import card, cardCD, cardN
from cardclasses import *


testDates = {}
testDates['javerage'] = [
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
]


# Both start and end dates are inclusive
cardList_javerage = [
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

]

cardList_none = []


cardLibrary = {}
cardLibrary['javerage'] = cardListToDict(cardList_javerage)
cardLibrary['none'] = cardListToDict(cardList_none)
