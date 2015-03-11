#!/usr/bin/python

# If you want to change the expected data you're testing against, 
# edit cards.py
# If you 

from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
from myuw_selenium.test.cardtestclass import co_test


# First day of winter quarter
@on_platforms()
class test_javerage_20130107(co_test, SeleniumLiveServerTestCase):
    date = '2013-01-07'

# Spring future quarter card moves to bottom
@on_platforms()
class test_javerage_20130110(co_test, SeleniumLiveServerTestCase):
    date = '2013-01-10'

# One week into quarter +1 day, textbook card disappears
@on_platforms()
class test_javerage_20130115(co_test, SeleniumLiveServerTestCase):
    date = '2013-01-15'

# First day of P1 registration for spring 2013
# Keep in mind javerage is already registered
@on_platforms()
class test_javerage_20130215(co_test, SeleniumLiveServerTestCase):
    date = '2013-02-15'

# Last day of classes for winter 2013
@on_platforms()
class test_javerage_20130315(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-15'

# Finals begin, i.e. last day of classes plus one day
@on_platforms()
class test_javerage_20130316(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-16'

# Last day of finals 
@on_platforms()
class test_javerage_20130321(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-21'

# Spring break begins
@on_platforms()
class test_javerage_20130322(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-22'

# Day before grade submission deadline
@on_platforms()
class test_javerage_20130325(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-25'

# Grade submission deadline
@on_platforms()
class test_javerage_20130326(co_test, SeleniumLiveServerTestCase):
    date = '2013-03-26'

# Quarter switch
#@on_platforms()
#class test_10_quarterSwitch(co_test, SeleniumLiveServerTestCase):
#    date = '2013-03-27'



