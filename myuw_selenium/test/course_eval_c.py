from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


from myuw_selenium.test.card_tests_c import CardTest

import time
import re
import datetime        

# General Test Class
class CourseEvalTest(CardTest):

    def setUp(self):
        CardTest.setUp(self)

        if not hasattr(self, 'all_courses'):
            self.all_courses = False

    def getCardObjects(self):
        time.sleep(2)        
        card_objects = self.getElements("div#CourseCard div.card")

        card_objects_dict = {}
        for element in card_objects:
            class_title = element.get_attribute('data-identifier')
            
            # Only get cards named in test
            if self.all_courses or (class_title in self.courses):
                card_objects_dict[class_title] = element

        return card_objects_dict

    def safeEnc(self, string):
        return str(string.encode("utf8"))



class EvalsShownTest(CourseEvalTest):
    def _test(self):
        card_objects = self.getCardObjects()
        
        for course in card_objects.keys():
                self.assertIsInstance(card_objects[course].find_element_by_css_selector("div.myuw-course-eval"), WebElement)

class EvalsNotShownTest(CourseEvalTest):
    def _test(self):
        card_objects = self.getCardObjects()

        for course in card_objects.keys():
            with self.assertRaises(NoSuchElementException):
                card_objects[course].find_element_by_css_selector("div.myuw-course-eval")


class LinksTest(CourseEvalTest):
    def _test(self):
        card_objects = self.getCardObjects()

        for course in card_objects.keys():
            links = {}
            link_elements = card_objects[course].find_elements_by_css_selector("div.myuw-course-eval a")
            for link in link_elements:
                links[self.safeEnc(link.text)] = link.get_attribute("href")

            self.assertEqual(sorted(self.links[course]), sorted(links))

class CloseDateTest(CourseEvalTest):
    def _test(self):
        card_objects = self.getCardObjects()

        for course in card_objects.keys():
            element = card_objects[course]
            text = element.find_element_by_css_selector("span.myuw-eval-close-date").text

            pattern = re.compile('^Submit your evaluation between ([A-za-z]{3} [0-9]{1,2}) to ([A-za-z]{3} [0-9]{1,2}).*$')
            match   = re.match(pattern, text)
            
            self.assertEqual(self.dates[course], [self.date_from_string(match.group(1)), self.date_from_string(match.group(2))])

    def date_from_string(self, date_string):
        month = date_string.split(' ')[0]
        day   = date_string.split(' ')[1]

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return datetime.date(2013, months.index(month) + 1, int(day))
    
class InstructorNameTest(CourseEvalTest):
    def _test(self):
        card_objects = self.getCardObjects()

        for course in card_objects.keys():
            name_elements = card_objects[course].find_elements_by_css_selector("ul.myuw-eval-list li.myuw-eval-list-item a")
            
            for element in name_elements:
                self.assertIn(' '.join(self.safeEnc(element.text).split(' ')[1:]), self.names[course])
            

class TabAccessTest(CourseEvalTest):
    def _test(self):
        self.send_tab = ActionChains(self.driver).send_keys(Keys.TAB)
        
        card_objects = self.getCardObjects()

        for course in card_objects.keys():
            card = card_objects[course]
            hidden_elements = card.find_elements_by_css_selector("div.slide-hide *")

            # Generate hash list (faster comparisons)
            hashes = []
            for element in hidden_elements:
                hashes.append(hash(element))
                
            start_element = self.driver.switch_to.active_element

            # Check first element not supposed to be hidden
            self.assertTrue(start_element not in hidden_elements)
            self.send_tab.perform()

            while self.driver.switch_to.active_element != start_element:
                element = self.driver.switch_to.active_element
                if (hash(element) in hashes):
                    self.assertFalse(element in hidden_elements,
                                     msg=("Element supposed to be hidden\nTag: %s\nText: %s\nClass: %s\nID: %s" %
                                          (element.tag_name, element.text, element.get_attribute('class'), element.get_attribute('id'))))
                    
                self.send_tab.perform()
