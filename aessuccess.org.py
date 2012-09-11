#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

from clint import args
from clint.textui import colored, puts

import keyring, sys


user = args.get(0)

if user is None:
    puts(colored.red('You must supply a username like "python aessuccess.org.py nick"'))
    sys.exit()

key = keyring.get_password('aessuccess.org', user)

puts(colored.blue('AES ({})'.format(user)))

if key is None:
    puts(colored.red("You must store the password for {} in your keyring's backend.".format(user)))
    puts('See: http://pypi.python.org/pypi/keyring/#configure-your-keyring-lib')
    sys.exit()

b = webdriver.Firefox()
b.get('http://aessuccess.org/')

username = b.find_element_by_css_selector('input#username')
username.send_keys(user)
username.submit()

# We need to catch whether or not a security question has been asked here, but it's tricky
# to get AES to think we're an unrecognized computer.

def _element_available(element):
    def callback(browser):
        try:
            browser.find_element_by_css_selector(element)
        except NoSuchElementException:
            return False
        else:
            return True
    return callback

WebDriverWait(b, timeout=10).until(_element_available('input#password'))

password = b.find_element_by_css_selector('input#password')
password.send_keys(key)
password.submit()

WebDriverWait(b, timeout=10).until(_element_available('table.paymentSummaryTable tbody tr.trCurrentPayment span.amount'))

amount = b.find_element_by_css_selector('table.paymentSummaryTable tbody tr.trCurrentPayment span.amount')

print 'AES ({}): {}'.format(user, amount.text)

b.quit()
