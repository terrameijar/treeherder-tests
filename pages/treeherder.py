# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.keys import Keys

from pages.base import Base
from pages.page import Page
from pages.page import PageRegion


class TreeherderPage(Base):

    _active_watched_repo_locator = (By.CSS_SELECTOR, '#watched-repo-navbar button.active')
    _mozilla_central_repo_locator = (By.CSS_SELECTOR, '#th-global-navbar-top a[href*="mozilla-central"]')
    _repos_menu_locator = (By.ID, 'repoLabel')
    _result_sets_locator = (By.CSS_SELECTOR, '.result-set:not(.row)')
    _unchecked_repos_links_locator = (By.CSS_SELECTOR, '#repoLabel + .dropdown-menu .dropdown-checkbox:not([checked]) + .dropdown-link')
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')
    _action_menu_dropdown_locator = (By.CSS_SELECTOR, ".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > button:nth-child(1)")
    _top_of_range_link_locator =  (By.CSS_SELECTOR,".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(7) > a:nth-child(1)")
    _bottom_of_range_link_locator = (By.CSS_SELECTOR, ".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(8) > a:nth-child(1)")

    def wait_for_page_to_load(self):
        Wait(self.selenium, self.timeout).until(
            lambda s: self.unclassified_failure_count > 0)
        return self

    def set_resultset_as_top_of_range(self):
        self.selenium.find_element(*self._action_menu_dropdown_locator).click()
        self.selenium.find_element(*self._top_of_range_link_locator).click()

    def set_resultset_as_bottom_of_range(self):
        self.selenium.find_element(*self._action_menu_dropdown_locator).click()
        self.selenium.find_element(*self._bottom_of_range_link_locator).click()

    @property
    def active_watched_repo(self):
        return self.selenium.find_element(*self._active_watched_repo_locator).text

    @property
    def job_details(self):
        return self.JobDetails(self)

    @property
    def pinboard(self):
        return self.Pinboard(self)

    @property
    def result_sets(self):
        return [self.ResultSet(self, el) for el in self.find_elements(self._result_sets_locator)]

    @property
    def unchecked_repos(self):
        return self.selenium.find_elements(*self._unchecked_repos_links_locator)

    @property
    def unclassified_failure_count(self):
        return int(self.selenium.find_element(*self._unclassified_failure_count_locator).text)

    def open_next_unclassified_failure(self):
        el = self.selenium.find_element(*self._result_sets_locator)
        Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
        el.send_keys('n')
        Wait(self.selenium, self.timeout).until(lambda s: self.job_details.job_result_status)

    def open_perfherder_page(self):
        self.header.switch_page_using_dropdown()

        from perfherder import PerfherderPage
        return PerfherderPage(self.base_url, self.selenium).wait_for_page_to_load()

    def open_repos_menu(self):
        self.selenium.find_element(*self._repos_menu_locator).click()

    def pin_using_spacebar(self):
        el = self.selenium.find_element(*self._result_sets_locator)
        Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
        el.send_keys(Keys.SPACE)
        Wait(self.selenium, self.timeout).until(lambda _: self.pinboard.is_pinboard_open)

    def select_mozilla_central_repo(self):
        # Fix me: https://github.com/mozilla/treeherder-tests/issues/43
        self.open_repos_menu()
        self.selenium.find_element(*self._mozilla_central_repo_locator).click()
        self.wait_for_page_to_load()

    def select_random_repo(self):
        self.open_repos_menu()
        repo = random.choice(self.unchecked_repos)
        repo_name = repo.text
        repo.click()
        Wait(self.selenium, self.timeout).until(
            lambda s: self._active_watched_repo_locator == repo_name)
        return repo_name

    class ResultSet(PageRegion):

        _datestamp_locator = (By.CSS_SELECTOR, '.result-set-title-left > span a')
        _jobs_locator = (By.CLASS_NAME, 'job-btn')
        _pin_all_jobs_locator = (By.CLASS_NAME, 'pin-all-jobs-btn')

        @property
        def datestamp(self):
            return self.find_element(self._datestamp_locator).text

        @property
        def jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(self._jobs_locator)]

        def pin_all_jobs(self):
            return self.find_element(self._pin_all_jobs_locator).click()

        def view(self):
            return self.find_element(self._datestamp_locator).click()

        class Job(PageRegion):

            def click(self):
                self._root.click()
                Wait(self.selenium, self.timeout).until(
                    lambda _: self.page.job_details.job_result_status)

            @property
            def symbol(self):
                return self._root.text

    class JobDetails(PageRegion):

        _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span:nth-child(2)')
        _logviewer_button_locator = (By.ID, 'logviewer-btn')
        _pin_job_locator = (By.ID, 'pin-job-btn')
        _job_details_panel_locator = (By.ID, 'job-details-panel')

        @property
        def job_result_status(self):
            return self.selenium.find_element(*self._job_result_status_locator).text

        def open_logviewer(self):
            self.selenium.find_element(*self._job_details_panel_locator).send_keys('l')
            window_handles = self.selenium.window_handles
            for handle in window_handles:
                self.selenium.switch_to.window(handle)
                self.selenium.implicitly_wait(1)
            return LogviewerPage(self.base_url, self.selenium)

        def pin_job(self):
            el = self.selenium.find_element(*self._pin_job_locator)
            Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
            el.click()

    class Pinboard(PageRegion):

        _root_locator = (By.ID, 'pinboard-panel')

        _clear_all_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(4)')
        _open_save_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .save-btn-dropdown')
        _jobs_locator = (By.CLASS_NAME, 'pinned-job')
        _pinboard_remove_job_locator = (By.CSS_SELECTOR, '#pinned-job-list .pinned-job-close-btn')

        @property
        def selected_job(self):
            return next(j for j in self.jobs if j.is_selected)

        @property
        def jobs(self):
            return [self.Job(self.page, el) for el in self.find_elements(self._jobs_locator)]

        @property
        def is_pinboard_open(self):
            return self.is_element_visible(self._root_locator)

        def clear_pinboard(self):
            el = self.selenium.find_element(*self._open_save_menu_locator)
            el.click()
            Wait(self.selenium, self.timeout).until(lambda _: el.get_attribute('aria-expanded') == 'true')
            self.selenium.find_element(*self._clear_all_menu_locator).click()

        class Job(PageRegion):

            @property
            def is_selected(self):
                return 'selected-job' in self._root.get_attribute('class')

            @property
            def symbol(self):
                return self._root.text


class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        Wait(self.selenium, self.timeout).until(
            lambda s: self.is_element_visible(self._job_header_locator))

    @property
    def is_job_status_visible(self):
        return self.is_element_visible(self._job_header_locator)
