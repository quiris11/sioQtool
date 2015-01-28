#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#
from __future__ import print_function
import argparse
import os
import re
import sys
import shutil
import difflib
import urllib
import urllib2

parser = argparse.ArgumentParser()
parser.add_argument("--move",
                    help="move reports to 'src' directory",
                    action="store_true")
parser.add_argument("--compare",
                    help="compare new reports with old reports",
                    action="store_true")
args = parser.parse_args()

doc_dir = os.path.join(os.path.expanduser('~'), 'cie_faqs')
dir_list = os.listdir(doc_dir)

if not os.path.exists(os.path.join(doc_dir, 'src')):
    os.makedirs(os.path.join(doc_dir, 'src'))

faq_list = [
    ['d2130071daf3ac8b056c519676c170c6', 'Dane zbiorcze'],
    ['75f530437b42e0aaa0a1f47464b1c532', 'Instalacja aplikacji'],
    ['f8efee67d2f31c13af12c477c53a59d3', 'Jednostki pozarejestrowe'],
    ['3626b333b7f28d6a45020d95d6b7b56a', 'Logowanie Reset hasła'],
    ['97284232a4b135ede6961ac90cc88c94', 'Nauczyciel'],
    ['29cce7c8e6b7c7177c7af982038d5d23', 'Podmiot'],
    ['533e2332623ad9c93e5a3bd56f93c8af', 'Praca z aplikacją'],
    ['f6f8005c3b7549db834e2c0c6972c91f', 'RSPO'],
    ['4ec64997463410d36630e037939875c6', 'Sprawozdawczość i statystyka'],
    ['423d2ab72b00b1e3a0b295d3e757fa86', 'Strefa dla zalogowanych'],
    ['58806385b55f0ae7214b1528880cdb6f', 'Uczeń'],
    ['d5468199a76795f7842aa9b837fcffe0', 'Wnioski o nadanie upoważnienia']
]


def get_faq(category):
    url = 'http://sio.men.gov.pl/dodatki/sio2_support/index.php'
    data = urllib.urlencode({
        'param': 'Support_htmlContent',
        'phrase': '',
        'category': category,
        'searchMode': 'undefined'
    })
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()


def compare_csvs(dir_list):
    for item in dir_list:
        if os.path.isdir(os.path.join(doc_dir, item)) or item == '.DS_Store':
            continue
        print('*** ' + item + ' ***')
        try:
            with open(os.path.join(doc_dir, 'src', item), 'r') as f:
                lines1 = f.read().split('\n')
            with open(os.path.join(doc_dir, item), 'r') as f:
                lines2 = f.read().split('\n')
                for line in difflib.unified_diff(
                    lines1, lines2,
                    fromfile='stary: ' + doc_dir + '/src/' + item,
                    tofile='nowy: ' + doc_dir + '/' + item,
                    lineterm='', n=0
                ):
                    print(line)
        except IOError:
            print('* Error')
            continue
        print('* OK')

if args.move:
    print('* Moving faqs to src directory...')
    for file in dir_list:
        try:
            shutil.copyfile(os.path.join(doc_dir, file),
                            os.path.join(doc_dir, 'src', file))
        except IOError:
            continue
    sys.exit()

if args.compare:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('* Comparing new faqs with old faqs...')
    compare_csvs(dir_list)
    sys.exit()

for faq in faq_list:
    bs = get_faq(faq[0])
    bs = '\n'.join(bs.split('\r\n')[:-10])
    bs = re.sub(
        r'<div class="question">(.+)</div>',
        r'<p><b>\1</b></p>',
        bs
    )
    bs = re.sub(
        r'<div class="answer">(.+?)</div>',
        r'<p>\1</p>',
        bs,
        flags=re.DOTALL
    )
    bs = bs.replace('<div class="kit kit_bg1">',
                    '<div style="background:#eee; border:0px solid #ccc; '
                    'padding:5px 10px">')
    bs = bs.replace('<div class="kit kit_bg0">',
                    '<div style="background:#f9f9f9; '
                    'border:0px solid #ccc; '
                    'padding:5px 10px">')
    bs = bs.replace('&quot;&quot;', '&quot;')
    bs = bs.replace('„', '&quot;')
    bs = bs.replace("\\'", '&quot;')
    bs = bs.replace("\\&quot;", '&quot;')
    bs = bs.replace('>Pyt.', '>Pyt. ')
    bs = bs.replace('\n', '<br />\n')
    bs = bs.replace('><br />', '>')
    with open(os.path.join(doc_dir, faq[1] + '.html'), 'w') as f:
        print('* Writing: %s...' % (faq[1] + '.html'))
        f.write(
            '<p><strong>UWAGA! Niżej opublikowane pytania i odpowiedzi '
            'zostały skopiowane z oryginalnego źródła: '
            '<a href="http://sio.men.gov.pl/index.php/pomoc/faqs">'
            'http://sio.men.gov.pl/index.php'
            '/pomoc/faqs</a></strong></p>'
        )
        f.write(bs)
