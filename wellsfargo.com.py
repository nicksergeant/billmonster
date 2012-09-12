#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver

from clint import args
from clint.textui import colored, puts

import keyring, sys


# Get the username from the command line arguments.
user = args.get(0)

# Must supply username.
if user is None:
    puts(colored.red('You must supply a username like "python wellsfargo.com.py nick"'))
    sys.exit()

# Get the user's password from the password backend.
key = keyring.get_password('wellsfargo.com', user)

# If the key doesn't exist in the password backend.
if key is None:
    puts(colored.red("You must store the password for {} in your keyring's backend.".format(user)))
    puts('See: http://pypi.python.org/pypi/keyring/#configure-your-keyring-lib')
    sys.exit()

# Log what we're currently working on.
puts(colored.blue('Wells Fargo: ({})'.format(user)))

# Init the WebDriver.
b = webdriver.Firefox()
b.get('https://www.wellsfargo.com/')

# Find the username field on the page.
username = b.find_element_by_css_selector('input#userid')
username.send_keys(user)

# Find the password field on the page.
password = b.find_element_by_css_selector('input#password')
password.send_keys(key)
password.submit()

# Helper function to check whether an element exists yet on the page.
def _element_available(element):
    def callback(browser):
        try:
            browser.find_element_by_css_selector(element)
        except NoSuchElementException:
            return False
        else:
            return True
    return callback

# Wait for an account list.
try:
    WebDriverWait(b, timeout=10).until(_element_available('a.account'))
except TimeoutException:
    puts(colored.red("Couldn't find any accounts for that username."))
    b.quit()
    sys.exit()

# Click the first account.
b.find_element_by_css_selector('a.account').click()

amount = b.find_element_by_css_selector('table#balanceDetails td.topRow a')

print 'Wells Fargo ({}): {}'.format(user, amount.text)

b.quit()
