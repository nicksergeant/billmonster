#!/usr/bin/python

from ConfigParser import ConfigParser
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

import os


config = ConfigParser()
config.read(os.path.expanduser('~/.billmonster'))

def main():

    from aessuccess import aessuccess
    from att import att
    from bankofamerica import bankofamerica
    from capitalone import capitalone
    from wellsfargo import wellsfargo

    # Providers map.
    PROVIDERS = {
        'aessuccess': aessuccess,
        'att': att,
        'bankofamerica': bankofamerica,
        'capitalone': capitalone,
        'wellsfargo': wellsfargo,
    }

    # Init the WebDriver.
    browser = webdriver.Firefox()

    for account in config._sections:

        # Grab the provider and the usernames.
        provider = account
        usernames = config._sections[account]['users']
        usernames = [x.strip() for x in usernames.split(',')]

        # Run the script for each account user.
        for user in usernames:
            PROVIDERS[provider](user, False, browser)

    browser.quit()


# Helper function to check whether an element exists yet on the page.
def _element_available(browser, element):
    def callback(browser):
        try:
            browser.find_element_by_css_selector(element)
        except NoSuchElementException:
            return False
        else:
            return True
    return callback


if __name__ == '__main__':
    main()
