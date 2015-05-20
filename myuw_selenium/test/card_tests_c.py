from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase
from selenium.webdriver.remote.webelement import WebElement

# Element Retrevial
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from unittest2 import TestCase
from selenium import webdriver
import pyvirtualdisplay

# General Test Class
class CardTest():

    def setUp(self):
        SeleniumLiveServerTestCase.setUp(self)

        #**********#

        # self.live_server_url = "http://0.0.0.0:8000"
        
        # self.driver  = webdriver.PhantomJS()
        # self.driver.set_window_size(800, 600)
        
        # self.display = pyvirtualdisplay.Display(visible = 1, size = (800, 600))
        # self.display.start()

        #**********#
        
        
        # Override functions
        if hasattr(self, 'user'):
            self.setUser()

        if hasattr(self, 'date'):
            self.setDate()

        # Browse to landing page
        self.driver.get(self.live_server_url + '/mobile/landing')

        #def tearDown(self):
        #self.driver.quit()
        #self.display.stop()
        
    def setUser(self):
        self.driver.get(self.live_server_url + '/users/')
        element = self.driver.find_element_by_xpath("//input[@name='override_as']")
        element.clear()
        element.send_keys(self.user)
        element.submit()
        time.sleep(2)
        
    def setDate(self):
        self.driver.get(self.live_server_url + '/mobile/admin/dates/')
        element = self.driver.find_element_by_xpath("//input[@name='date']")
        element.clear()
        element.send_keys(self.date)
        element.submit()
        time.sleep(2)

        
    def getCardObject(self):
        card_object = self.getElement(self.card_name, by_method=By.ID)
        # Raise AssertionError if card is not displayed
        if (not card_object.is_displayed()):
            raise AssertionError('Card not displayed on landing page')

        return card_object

    def getElement(self, selector, by_method=By.CSS_SELECTOR):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_method, selector)))
        WebDriverWait(self.driver, 10).until(EC.visibility_of(element))
        return element

    def getElements(self, selector, by_method=By.CSS_SELECTOR):
        elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((by_method, selector)))
        for element in elements:
            try:
                WebDriverWait(self.driver, 2).until(EC.visibility_of(element))
            except TimeoutException:
                elements.remove(element)

        return elements


# Helper Functions
def create_test_class(_class):

    @on_platforms()
    class CardTestWithData(_class, SeleniumLiveServerTestCase):
    #class CardTestWithData(_class, TestCase):
        def __str__(self):
            return _class.__name__ + ": " + self.test_name

    return [CardTestWithData_1]


def create_test_from_test(data):
    tests = [] 
    
    # Get test class
    _class = data['test']
    del data['test']

    test_classes = create_test_class(_class)

    index = 1
    for _test in test_classes:
        # Rename testn
        setattr(_test, 'test_' + data['test_name'], _class._test)
        
        # Set attributes
        for key in data.keys():
            setattr(_test, key, data[key])

        # Add to tests
        tests.append(_test)
        index += 1
        
    return tests
