#!/usr/bin/python

# If you want to change the expected data you're testing against, 
# edit cards.py
# If you want to changes the dates to be tested, edit this file. 

from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
from myuw_selenium.test.cardtestclass import co_test
from myuw_selenium.test.cards import testDates

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
