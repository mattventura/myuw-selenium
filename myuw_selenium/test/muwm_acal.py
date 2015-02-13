#!/usr/bin/python


from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
import time
import datetime
from selenium.webdriver.common.keys import Keys

# Set the default year here
# Probably won't change for the forseeable future
defyear = 2013

# Class for an Academic Calendar test object
# This is the base class
# Scenarios need to subclass this first, then SeleniumLiveServerTestCase
# They must also provide the 'user' and 'date' properties. 
class AcalTestClass(object):
    # Setup function
    def setUp(self):
        # Need to call the "parent"'s setup, but 
        # it's not actually a parent of this class so 
        # we can't use super(). It's not a parent because
        # we don't want this class actually running. 
        SeleniumLiveServerTestCase.setUp(self)

        # Get test server URL which is provided to us by
        # SeleniumLiveServerTestCase. 
        self.urlbase = self.live_server_url
        # Formulate page URLs from base URL
        self.datesPage = self.urlbase + '/mobile/admin/dates/'
        self.userPage = self.urlbase + '/users/'
        self.landingPage = self.urlbase + '/mobile/landing/'
        # Set our own date and username
        self.setDate(self.date)
        self.setUser(self.user)
        # Go to landing page
        self.browseLanding()
        # Make datetime object so we can compare it to other dates
        self.dateTime = datetime.datetime.strptime(self.date, '%Y-%m-%d')

    # Navigate to date override page, put in our custom date
    def setDate(self, date):
        self.driver.get(self.datesPage)
        time.sleep(.2)
        e = self.driver.find_element_by_xpath('//input[@name="date"]')
        e.send_keys(date + '\n')
        time.sleep(.2)
        self.dateStr = date

    # Navigate to user override page, set username
    def setUser(self, user):
        driver = self.driver
        driver.get(self.userPage)
        time.sleep(.2)
        namebox = driver.find_element_by_name('override_as')
        namebox.send_keys(user + Keys.RETURN)
        time.sleep(.2)
    
    # Navigate to landing page
    def browseLanding(self):
        self.driver.get(self.landingPage)
        time.sleep(1)

    # Actual calendar test
    # Makes sure that there are no more than 3 dates
    # on the landing page's calendar display.
    def test_calendar(self):
        events = getCalEvents(self.driver)
        dates = set()
        for e in events:
            dates.add(self.getEventDate(e))
        self.assertLessEqual(len(dates), 3)
        
    # Given an event, get the date that it occurs on,
    # or today's date if it is a spanning event that spans
    # across today.
    # Perform sanity checks to make sure the event isn't
    # a past event. 
    def getEventDate(self, event):
        if event.span:
            dateEvent = event.dateBegin
            dateCurrent = self.dateTime
            if self.isDatePast(event.dateEnd):
                self.fail('%s occured in the past (now is %s)' %(event, dateCurrent))
            if dateEvent > dateCurrent: 
                return dateEvent
            else:
                return dateCurrent
            # Sanity check

        else:
            dateEvent = event.dateBegin
            dateCurrent = self.dateTime

            if self.isDatePast(dateEvent):
                self.fail('%s occured in the past (now is %s)' %(event, dateCurrent))
            else:
                return dateEvent

    # Take a guess as to whether a date is actually in the past, 
    # and not just year-span confusion
    def isDatePast(self, date):
        curDate = self.dateTime
        newDate = date

        if newDate >= curDate:
            return False
        else:
            delta = newDate - curDate
            # Use 200 days in the past as our threshold
            if delta.days < -200:
                return False
            else:
                return True

        


# Class for an event as seen on the calendar
class calEvent(object):
    # Initialize based on a web element
    def __init__(self, e):
        datePart = e.find_element_by_class_name('acal-banner-date')
        dateStr = datePart.text
        dateStr = dateStr.replace('June', 'Jun').replace('July', 'Jul').replace('Sept', 'Sep')
        dateSplit = dateStr.split(' - ') # Split date ranges into beginning and end
        # Handle spanning events
        if len(dateSplit) == 2:
            dateBegin = dateSplit[0]
            dateEnd = dateSplit[1]
            self.span = True
            # Turn dates into time structures
            self.dateBegin = datetime.datetime.strptime(dateBegin + str(defyear), '%b %d%Y')
            # End date can either be Month and Day or just Day if the end date is the same month
            endParts = dateEnd.split(' ')
            if len(endParts) == 2:
                self.dateEnd = datetime.datetime.strptime(dateEnd + str(defyear), '%b %d%Y')
            elif len(endParts) == 1:
                beginParts = dateBegin.split(' ')
                month = beginParts[0]
                self.dateEnd = datetime.datetime.strptime(month + dateEnd + str(defyear), '%b%d%Y')
            if self.dateEnd < self.dateBegin:
                self.dateEnd = self.dateEnd.replace(year = self.dateEnd.year + 1)
                
        # Handle non-spanning events
        elif len(dateSplit) == 1:
            dateBegin = dateSplit[0]
            # Remove (Sunday) thing that you get when the event occurs within a wek
            dateBegin = dateBegin.split(' (')[0] 
            # Make datetime object out of date
            self.dateBegin = datetime.datetime.strptime(dateBegin + str(defyear), '%b %d%Y')
            self.span = False
        else:
            raise Exception('Invalid date string %s' %dateStr)

        # Label is always a link (the only link) so use this to get the label
        labelElement = e.find_element_by_tag_name('a')
        self.label = labelElement.text
        self.url = labelElement.get_attribute('href')

    def __str__(self):
        if self.span:
            return 'Span %s to %s "%s"' %(self.dateBegin, self.dateEnd, self.label)
        else:
            return 'Event %s "%s"' %(self.dateBegin, self.label)

    __repr__ = __str__

# Get all calendar events on the current page, return an list of them
# as calEvent instances
def getCalEvents(driver):
    el = driver.find_elements_by_xpath('//ul[@class="acal-banner-list"]/li/div')
    events = []
    for e in el:
        events.append(calEvent(e))

    return events
    
# Object to hold a date and username to test the calendar with
class calScenario(object):
    
    def __init__(self, user, date):
        self.user = user
        self.date = date

    @property
    def name(self):
        return self.date.replace('-', '_')
        
# Laziness
c = calScenario

# List of scenarios
# To define a new date to test at, put it here
dates = [
    c('javerage', '2013-01-02'),
    c('javerage', '2013-01-15'),
    c('javerage', '2013-04-15'),
    c('javerage', '2013-04-25'),
    c('javerage', '2013-05-30'),
    #c('javerage', ''),
    #c('javerage', ''),
    c('javerage', '2013-07-25'),
    c('javerage', '2013-12-12'),
    c('javerage', '2013-12-16'),
    # This one fails, guess the date is too far forward
    #c('javerage', '2013-12-24'), 
    #c('javerage', ''),
]

# Create a test class for a particular calScenario
def createTestClass(scenario):
    
    @on_platforms()
    class scenarioClass(AcalTestClass, SeleniumLiveServerTestCase):
        date = scenario.date
        user = scenario.user

    return [scenarioClass_1]

# Dynamically generate test classes for each calScenario in dates
for d in dates:
    vars()['class_' + d.name] = createTestClass(d)[0]
    # unittest will somehow pick up the test class if we don't
    # explicitly delete it
    del scenarioClass_1
     
