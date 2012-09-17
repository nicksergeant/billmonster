#!/usr/bin/env python

from ConfigParser import ConfigParser

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver

from billmonster import _element_available

from clint import args
from clint.textui import colored, puts

import keyring, os, sys


config = ConfigParser()
config.read(os.path.expanduser('~/.billmonster'))

def bankofamerica(user=None, quit_when_finished=True, browser=None):

    if not user:
        # Get the username from the command line arguments.
        user = args.get(0)

    # Must supply username.
    if user is None:
        puts(colored.red('You must supply a username like "python bankofamerica.py nick"'))
        sys.exit()

    # Get the user's password from the password backend.
    key = keyring.get_password('bankofamerica.com', user)

    # If the key doesn't exist in the password backend.
    if key is None:
        puts(colored.red("You must store the password for {} in your keyring's backend.".format(user)))
        puts('See: http://pypi.python.org/pypi/keyring/#configure-your-keyring-lib')
        sys.exit()

    # Log what we're currently working on.
    puts(colored.blue('\nBank of America ({})'.format(user)))

    if not browser:
        # Init the WebDriver.
        b = webdriver.Firefox()
    else:
        b = browser

    b.get('https://www.bankofamerica.com/')

    # Find the username field on the page.
    username = b.find_element_by_css_selector('input#id')
    username.send_keys(user)

    # Get the state out of the user's config.
    state_config = config._sections['bankofamerica']['state']

    # Select the correct state.
    state = b.find_element_by_css_selector('option[value="{}"]'.format(state_config))
    state.click()

    username.submit()

    # If we have a password field, continue. Otherwise, wait to see if we are
    # being asked a security question.
    try:
        WebDriverWait(b, timeout=10).until(_element_available(b, 'input#tlpvt-passcode-input'))
    except TimeoutException:
        WebDriverWait(b, timeout=10).until(_element_available(b, 'input#tlpvt-challenge-answer'))

    # If we have a password field now, fill it with the key and submit the form.
    try:
        password = b.find_element_by_css_selector('input#tlpvt-passcode-input')
        password.send_keys(key)
        password.submit()
    except NoSuchElementException:

        # We need to hit the keychain for the security question.
        answer = b.find_element_by_css_selector('input#tlpvt-challenge-answer')
        question = b.find_element_by_css_selector('label[for="tlpvt-challenge-answer"]').text.strip()

        # The keychain name should be "username What is your mother's middle name", for example.
        keyAnswer = keyring.get_password('bankofamerica.com', '{} {}'.format(user, question))

        # Make sure we have an answer for the question.
        if keyAnswer is None:
            puts(colored.red("We couldn't find an answer for the question '{}' in your keyring's backend".format(question)))
            b.quit()
            sys.exit()

        # Fill the answer and submit.
        answer.send_keys(keyAnswer)
        answer.submit()

        # If we've answered correctly, now we have to wait for the password field.
        WebDriverWait(b, timeout=10).until(_element_available(b, 'input#tlpvt-passcode-input'))

        # Fill the password and submit.
        password = b.find_element_by_css_selector('input#tlpvt-passcode-input')
        password.send_keys(key)
        password.submit()

    # Finally, once we have the amount on the page, harvest it and print the result.
    #WebDriverWait(b, timeout=10).until(_element_available(b, 'table.paymentSummaryTable tbody tr.trCurrentPayment span.amount'))
    #amount = b.find_element_by_css_selector('table.paymentSummaryTable tbody tr.trCurrentPayment span.amount')

    #print 'Bank of America ({}): {}'.format(user, amount.text)

    if quit_when_finished:
        b.quit()

    return b


if __name__ == '__main__':
    bankofamerica()
