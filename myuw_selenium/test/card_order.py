from myuw_selenium.platforms import on_platforms, SeleniumLiveServerTestCase

@on_platforms()
class CardOrderTest(SeleniumLiveServerTestCase):
    """
    Tests the order and display of cards at various times in the quarter.
    """

    def test_card_order(self):
        from time import sleep
        # Allow longer failure messages
        self.maxDiff = None

        dates = [
            { 'date': "2013-04-07", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-08", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-21", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-22", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-25", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-26", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-04-29", 'user': 'none' }, # Needs to be none to have no registrations, otherwise RegStatusCard is hidden
            { 'date': "2013-05-30", 'user': 'none' }, # Same!
            { 'date': "2013-03-10", 'user': 'none' }, # Need to go back in time, otherwise autumn makes this break - Same though
            { 'date': "2013-03-11", 'user': 'none' }, # Need to go back in time, otherwise autumn makes this break

            { 'date': "2013-04-01", 'user': 'javerage' },
            { 'date': "2013-04-02", 'user': 'javerage' }, # Same!
            { 'date': "2013-04-03", 'user': 'javerage' }, # Future quarter moves to position 1
            { 'date': "2013-04-25", 'user': 'javerage' }, # Same!

            { 'date': "2013-06-07", 'user': 'javerage' }, # Same (ish)!
            { 'date': "2013-06-08", 'user': 'javerage' },
            { 'date': "2013-06-13", 'user': 'javerage' }, # Same!
            { 'date': "2013-06-15", 'user': 'javerage' },
            { 'date': "2013-08-27", 'user': 'javerage' }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-08-28", 'user': 'javerage' }, # Need to go to the future - spring's grade submission deadline is always today actual.
            { 'date': "2013-09-24", 'user': 'javerage' }, # Same
            { 'date': "2013-09-25", 'user': 'javerage' },
        ]

        correct_cards = [
            ['VisualScheduleCard', 'CourseCard', 'TuitionCard'], #  'date': "2013-04-07", 'user': 'none'
            ['SummerRegStatusCardA', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'],
            ['SummerRegStatusCardA', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'],
            ['VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'],
            ['VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'],
            ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'],
            ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard', 'SummerRegStatusCard1'], #  'date': "2013-04-29", 'user': 'none'
            ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'],
            ['RegStatusCard', 'VisualScheduleCard', 'CourseCard', 'TuitionCard'],
            ['VisualScheduleCard', 'CourseCard', 'TuitionCard'],

            ['FutureQuarterCardA', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard'],
            ['FutureQuarterCardA', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard'],
            ['VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['VisualScheduleCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],

            ['VisualScheduleCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['FinalExamCard', 'GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['FinalExamCard', 'GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['GradeCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard', 'AcademicCard', 'FutureQuarterCard1'],
            ['GradeCard', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'],
            ['GradeCard', 'VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'],
            ['VisualScheduleCard', 'TextbookCard', 'CourseCard', 'HFSCard', 'TuitionCard', 'LibraryCard'],
        ]

        # Not technically needed to make the tests pass, but cleans
        # up the failure messages a bit. 
        for l in correct_cards:
            for i in range(len(l)):
                l[i] = unicode(l[i])
                

        index = 0
        curUser = ''
        for val in dates:
            date = val["date"]
            user = val["user"]

            # Only switch users if necessary, saves a bit of time. 
            if user != curUser:
                self.driver.get(self.live_server_url + '/users/')
                element = self.driver.find_element_by_xpath("//input[@name='override_as']")
                element.clear()
                element.send_keys(user)
                element.submit()
                curUser = user

            self.driver.get(self.live_server_url + '/mobile/admin/dates/')
            element = self.driver.find_element_by_xpath("//input[@name='date']")
            element.clear()
            element.send_keys(date)
            element.submit()
            self.driver.get(self.live_server_url + '/mobile/landing/')
            # XXX - this is lame.  need to add something to wait on here instead
            sleep(2)
            title = self.driver.title
            self.assertEquals(self.driver.title, "MyUW Mobile Home")

            divs = self.driver.find_elements_by_css_selector("#landing_content > div")

            displayed = []
            for div in divs:
                if div.get_attribute("style") != "display: none;":
                    displayed.append(div.get_attribute("id"))

            cards = correct_cards[index]

            # Use this instead of checking for same length then checking each element
            self.assertEqual(cards, displayed, 'Incorrect set of cards on date %s' %date)

            index = index + 1
