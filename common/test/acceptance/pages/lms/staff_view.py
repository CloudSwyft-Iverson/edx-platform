"""
Staff view of courseware
"""
from bok_choy.page_object import PageObject


class StaffPage(PageObject):
    """
    View of courseware pages while logged in as course staff
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='#staffstatus').present

    @property
    def staff_status(self):
        """
        Return the current status, either Staff view or Student view
        """
        return self.q(css='#staffstatus').text[0]

    def open_staff_debug_info(self):
        """
        Open the staff debug window
        Return the page object for it.
        """
        self.q(css='a.instructor-info-action').first.click()
        staff_debug_page = StaffDebugPage(self.browser)
        staff_debug_page.wait_for_page()
        return staff_debug_page


class StaffDebugPage(PageObject):
    """
    Staff Debug modal
    """

    url = None

    def is_browser_on_page(self):
        return self.q(css='section.staff-modal').present

    def _click_link(self, link_text):
        for link in self.q(css='section.staff-modal a').execute():
            if link.text == link_text:
                return link.click()

        raise Exception('Could not find the {} link to click on.'.format(
            link_text))

    def reset_attempts(self):
        self._click_link('Reset Attempts')

    @property
    def idash_msg(self):
        self.wait_for_ajax()
        return self.q(css='#idash_msg').text
