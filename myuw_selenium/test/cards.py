#!/usr/bin/python

from myuw_selenium.test.cardclasses import card, cardCD, cardN
from cardclasses import *

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
