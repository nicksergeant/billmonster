#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from billmonster import _element_available

from clint import args
from clint.textui import colored, puts

import keyring, sys


def capitalone(user=None, quit_when_finished=True, browser=None):

    if not user:
        # Get the username from the command line arguments.
        user = args.get(0)

    # Must supply username.
    if user is None:
        puts(colored.red('You must supply a username like "python capitalone.py nick"'))
        sys.exit()

    # Get the user's password from the password backend.
    key = keyring.get_password('capitalone.com', user)

    # If the key doesn't exist in the password backend.
    if key is None:
        puts(colored.red("You must store the password for {} in your keyring's backend.".format(user)))
        puts('See: http://pypi.python.org/pypi/keyring/#configure-your-keyring-lib')
        sys.exit()

    # Log what we're currently working on.
    puts(colored.blue('\nCapital One: ({})'.format(user)))

    if not browser:
        # Init the WebDriver.
        b = webdriver.Firefox()
    else:
        b = browser

    b.get('https://www.capitalone.com/')

    # Only credit card accounts are supported at this time.
    account_type = b.find_element_by_css_selector('option[value="credit cards"]')
    account_type.click()

    # Find the username field on the page.
    username = b.find_element_by_css_selector('input#eos-userid')
    username.send_keys(user)

    # Find the password field on the page.
    password = b.find_element_by_css_selector('input#eos-password')
    password.send_keys(key)
    password.submit()

    # Wait for an account list.
    try:
        WebDriverWait(b, timeout=10).until(_element_available(b, 'table.dataTable'))
    except TimeoutException:
        puts(colored.red("Couldn't find any accounts for that username."))
        b.quit()
        sys.exit()

    amount = b.find_element_by_css_selector('table.dataTable tr.itemSummary td:nth-child(4) p')

    print 'Capital One ({}): {}'.format(user, amount.text)

    if quit_when_finished:
        b.quit()

    return b


if __name__ == '__main__':
    capitalone()
