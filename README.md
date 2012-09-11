# Bill Monster

![Nom](http://i.imgur.com/kYSmu.png)

The Bill Monster eats your bills and simply tells you what your current due balance is.

It uses Selenium to automate the process of logging into each provider and harvesting
the balances.

## Requirements

- brew install selenium-server-standalone
- pip install clint keyring selenium

## How it works

The script uses [keyring](http://pypi.python.org/pypi/keyring/), which uses a
local password storage backend to retrieve passwords. On OS X, the Keychain is used.

## Usage and supported providers

### AESSuccess.org:

    python aessuccess.org.py nick

The script checks the password backend for a password stored with the name
`aessuccess.org` and a username of `nick` and begins the login process.

AES requires security questions if you're logging in on a computer that isn't recognized.
The Bill Monster has built-in support for these. When you're running the script for the first
time, you'll see the security questions come on screen, and you'll need to add those to your
keychain to avoid holding up the script in subsequent runs. A sample keychain entry for an AES
security question:

    Name: aessuccess.org
    Kind: application password
    Account: nick *What is your mother's middle name?
    Where: aessuccess.org
    Password: Emmy Lou

...where `nick` is your username, and `Emmy Lou` is your mother's middle name.

If it is able to login successfully, it prints the following to stdout:

    AES (nick): $120.45
