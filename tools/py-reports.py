#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#
from __future__ import print_function
import os
import shutil
import getpass
from os.path import expanduser
from lxml import etree
import subprocess
import urllib
import urllib2
import sys
import re


home = expanduser("~")

XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
         'x': 'urn:schemas-microsoft-com:office:excel',
         'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

report_list = [
    ['6', 'rspo_aktywne.xls'],
    ['65', 'rspo_nieaktywne.xls'],
    ['61', 'ee_przedszk.xls'],
    ['62', 'ee_sp.xls'],
    ['63', 'obwody.xls'],
    ['64', 'zawody.xls']
]

fnull = open(os.devnull, 'w')
uname = raw_input("Username: ")
passwd = getpass.getpass()

url = 'https://sio.men.gov.pl/dodatki/strefa/index.php'
data = urllib.urlencode({
    'nazwaUzytkownika': uname,
    'hasloUzytkownika': passwd,
    'param': 'Start_login'
})
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
cookie = response.info()['Set-Cookie']

if cookie:
    print(cookie)

# sys.exit()
subprocess.check_call([
    'wget',
    '--delete-after',
    '--keep-session-cookies',
    '--save-cookies=my_cookies.txt',
    '--post-data=nazwaUzytkownika=%s&hasloUzytkownika=%s&param='
    'Start_login' % (uname, passwd),
    'https://sio.men.gov.pl/dodatki/strefa/index.php'
], stdout=fnull, stderr=subprocess.STDOUT)

for i in report_list:
    try:
        tree = etree.parse(os.path.join('%s/NSIO/%s' % (home, i[1])))
        title_old = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                               namespaces=XLSNS)[0]
    except:
        print('Error! Incorrect file: %s/NSIO/%s' % (home, i[1]))
        continue
    url = 'https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_' + i[0]
    print(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    req.add_header('Cookie', cookie)
    print(req)
    response = urllib2.urlopen(req)
    print(response.read())
    sys.exit()

    subprocess.check_call([
        'wget',
        '--load-cookies=my_cookies.txt',
        'https://sio.men.gov.pl/dodatki/strefa/index.php?'
        'param=Support_download_%s' % i[0],
        '--output-document=%s/NSIO/new_%s' % (home, i[1])
    ], stdout=fnull, stderr=subprocess.STDOUT)
    try:
        tree = etree.parse(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
        title_new = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                               namespaces=XLSNS)[0]
    except:
        print('Error! Incorrect file: %s/NSIO/new_%s' % (home, i[1]))
        os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
        continue
    print('Local file title: ' + title_old)
    print('Remote file title: ' + title_new)
    if title_old == title_new:
        print('Remote file: %s/NSIO/new_%s NOT upadated...' % (home, i[1]))
        os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
    else:
        print('Remote file: %s/NSIO/new_%s upadated. '
              'Replacing the old one...' % (home, i[1]))
        shutil.copyfile(os.path.join('%s/NSIO/new_%s' % (home, i[1])),
                        os.path.join('%s/NSIO/%s' % (home, i[1])))
        os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
os.remove(os.path.join('my_cookies.txt'))
fnull.close()
