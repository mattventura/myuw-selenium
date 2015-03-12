#!/usr/bin/python

# If you want to change the expected data you're testing against, 
# edit cards.py
# If you want to changes the dates to be tested, edit this file. 

from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
from myuw_selenium.test.cardtestclass import co_test

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

# Generate test classes based off the above data
for userName in testDates:
    dates = testDates[userName]
    for testDate in dates:
        class testClass(co_test, SeleniumLiveServerTestCase):
            date = testDate
            user = userName

        testClass.__name__ = 'test_%s_%s' %(userName, testDate)
        on_platforms()(testClass) 
        del testClass
