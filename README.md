# Bill Monster

![Nom](http://i.imgur.com/kYSmu.png)

The Bill Monster eats your bills and tells you what your current due balances are.

It uses Selenium to automate the process of logging into each provider and harvesting
the balances.

## Requirements

- `brew install selenium-server-standalone` (or via your favorite OS package manager)
- `pip install clint keyring selenium`

## How it works

The script uses [keyring](http://pypi.python.org/pypi/keyring/), which uses a
local password storage backend to retrieve passwords. On OS X, the Keychain is used by default.

## Account and username configuration

See the provided `.config` sample file in the repo. Copy that file to `~/.billmonster` and create
configuration sections for each provider you would like to use. Multiple accounts per provider
is also supported (see the sample).

## Password configuration

Use your [keyring](http://pypi.python.org/pypi/keyring/)'s password backend to store your passwords.

As an example, if I wanted to use the Wells Fargo provider, I would create an entry like this:

    Name: wellsfargo.com
    Account: nick
    Where: wellsfargo.com
    Password: o-hi-thar

## Usage

See below for using each individual provider script separately.

Otherwise, you can create a config (see above) and run the script:

    python billmonster.py
    
Once started, you'll see a line for each provider / account that it begins to process, like this:

    AES (nick)
    
If everything goes smoothly, the Bill Monster will then print the balance to stdout:

    AES (nick): $120.45
    
It'll then move on to the next account, and so on.

## Supported providers

### AESSuccess.org

    python aessuccess.py nick

The script checks the password backend for a password stored with the name
`aessuccess.org` and a username of `nick` and begins the login process if it finds one.

AES requires security questions if you're logging in on a computer that isn't recognized.
The Bill Monster has built-in support for these. When you're running the script for the first
time, you'll see the security questions come on-screen, and you'll need to add those to your
keychain to avoid holding up the script in subsequent runs. A sample keychain entry for an AES
security question:

    Name: aessuccess.org
    Kind: application password
    Account: nick *What is your mother's middle name?
    Where: aessuccess.org
    Password: Emmy Lou

...where `nick` is your username, and `Emmy Lou` is your mother's middle name.

### ATT.com

    python att.py 3155551234

Note: Your AT&T account username is probably your phone number.

### WellsFargo.com

    python wellsfargo.py nick

Currently Wells Fargo support is only for single loan accounts.

### Future supported providers

- AT&T
- Bank of America Credit Cards
- Capital One Credit Cards
- Tompkins Bank Credit Cards
- Citi Credit Cards
- Community Bank NA Loans
- ESL FCU Loans
- M&T Bank Loans
- Nelnet Student Loans
- Old Navy Credit Cards
- RG&E Gas & Electric Bills
- The Limited Credit Cards
- Time Warner Cable Bills
- Travelers Insurance Bills
- USAA Credit Cards
