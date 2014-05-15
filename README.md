walletinfo
==========

Multi-coin wallet info tool

```
Usage: wi.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --datadir=DATADIR     wallet directory (defaults to current directory
  --wallet=WALLETFILE   wallet filename (defaults to wallet.dat)
  --is-encrypted        check if wallet is encrypted
  --passphrase=PASSPHRASE
                        passphrase for the encrypted wallet
  --test-passphrase     test if passed passphrase is correct
  --determine-coin      tries to determine coin
  --list-keys           list private and public keys
  --list-public-keys    list only public keys
  --list-private-keys   list only private keys
  --list-contacts       lists wallet address book contacts
  --balances            list balances for each key
  --explore-url         print block explorer url for each address
```


Installation instructions
=========================

Dependencies:

Debian-based Linux:
```
 aptitude install build-essential python-dev python-bsddb3
```
Mac OS X:
```
 1. Install MacPorts from http://www.macports.org/
 2. sudo port install python27 py27-pip py-bsddb python_select
 3. sudo port select --set python python27
 4. sudo easy_install ecdsa
```

Windows:
```
 1. Install Python 2.7
 2. Install Twisted 11.0.0 for Py2.7, then Zope.Interface (a .egg file) for Py2.7: http://twistedmatrix.com/trac/wiki/Downloads

 3. Untested, proposed by TeaRex: install Zope.Interface from http://www.lfd.uci.edu/~gohlke/pythonlibs

 If this doesn't work, you will have to install the egg file:

 3(32bit). http://pypi.python.org/pypi/setuptools#downloads to install setuptools
 3(64bit). http://pypi.python.org/pypi/setuptools#windows to download, then run ez_setup.py

 4. Go to C:\Python27\Scripts
 5. Run easy_install.exe zope.interface-3.6.4-py2.7-win-amd64.egg
```