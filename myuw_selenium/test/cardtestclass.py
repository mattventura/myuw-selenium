#!/usr/bin/python

from myuw_selenium.test.cards import cardLibrary
from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
import datetime
import time
# URL suffixes
datePageSuffix = '/mobile/admin/dates/'
landingSuffix = '/mobile/landing/'
userSuffix = '/users/'

# The user that it will default to
# We don't override the user except when necessary
currentUser = ''

# Other tests should sublcass this as its first superclass, as well
# as SeleniumLiveServerTestCase
class co_test():
    
    # Default username
    #user = 'javerage'

    # Setup function. Calls SeleniumLiveServerTestCase so that it can do its
    # thing despite being overridden here. 
    def setUp(self):
        SeleniumLiveServerTestCase.setUp(self)
        
        # Formulate full URLs
        url = self.live_server_url
        self.datesPage = url + datePageSuffix
        self.landingPage = url + landingSuffix
        self.userPage = url + userSuffix
        self.dateObj = datetime.datetime.strptime(self.date, '%Y-%m-%d')

        # Pick the card library for our user
        self.cardLibrary = cardLibrary[self.user]

        # Set the correct username and date, then go to the landing
        self.setUser()

    # Override user to self.user, but only if we actually need to. 
    # If the desired username and current username are the same, we don't need
    # to do anything. 
    def setUser(self):
        global currentUser
        user = self.user
        if user != currentUser:
            self.chgUser(user)
            currentUser = user
        
    def chgUser(self, user):
        self.driver.get(self.userPage)
        time.sleep(.2)
        namebox = self.driver.find_element_by_xpath('//input[@name="override_as"]')
        namebox.send_keys(user + '\n')
        time.sleep(.2)

    # Set the date to the date at which our test is supposed
    # to take place. 
    def setToDate(self):
        self.setDate(self.date)

    # Set date to given date
    def setDate(self, date):
        self.driver.get(self.datesPage)
        time.sleep(.2)
        e = self.driver.find_element_by_xpath('//input[@name="date"]')
        e.send_keys(date + '\n')
        time.sleep(.2)
        self.dateSet = True

    # Browse the landing page
    def browseLanding(self):
        self.driver.get(self.landingPage)

    # Actually test our card display
    def test_card_order(self):
        #self.fail('blah')
        self.setToDate()
        self.browseLanding()
        self._testCards()


    # Test the cards currently on the page
    def _testCards(self):
        # Get all cards
        cards = self.driver.find_elements_by_xpath('//div[@id="landing_content"]/div')
        failText = ''
        for c in cards:
            #print('Card %s displayed: %s' %(c.get_attribute('id'), c.is_displayed()))
            # Get the actual name of the card
            cardName = c.get_attribute('id')
            try:
                # Try to find it in our library of expected cards
                cardObj = self.cardLibrary[cardName]
            except KeyError:
                # Card ID wasn't found in our library of cards
                # This is either a new card, a card with its ID changed, 
                # or a card that hasn't been programmed for yet. 
                print('Unknown card %s' %cardName)
                continue

            # Is the card displayed: Actual value
            isDisplayed = c.is_displayed()
            # Is the card displayed: Expected value
            expDisplayed = cardObj.shouldBeDisplayed(self.dateObj)

            # Check that the card is displayed iff it should be displayed
            if isDisplayed != expDisplayed:
                failText += 'Card %s (actual: %s, expected: %s)\n' %(cardName, isDisplayed, expDisplayed)

        if failText:
            failText = 'The following cards had issues on date %s: \n' %self.date + failText
            self.fail(failText)



