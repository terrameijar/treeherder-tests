# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.treeherder import TreeherderPage


def test_move_to_top_of_range(base_url, selenium):
    page = TreeherderPage(base_url, selenium).open()
    result_set = page.ResultSet(page)
    result_set.set_resultset_as_top_of_range()
    assert "&tochange=" in page.selenium.current_url


def test_move_to_bottom_of_range(base_url, selenium):
    page = TreeherderPage(base_url, selenium).open()
    result_set = page.ResultSet(page)
    result_set.set_resultset_as_bottom_of_range()
    assert "fromchange=" in page.selenium.current_url
