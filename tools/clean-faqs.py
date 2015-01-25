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
if not os.path.exists(os.path.join(doc_dir, 'out')):
    os.makedirs(os.path.join(doc_dir, 'out'))


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

for file in dir_list:
    if os.path.isdir(os.path.join(doc_dir, file)):
        continue
    with open(os.path.join(doc_dir, file), 'r') as f:
        bs = f.read()
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
        with open(os.path.join(doc_dir, 'out', file), 'w') as o:
            o.write(
                '<p><strong>UWAGA! Niżej opublikowane pytania i odpowiedzi '
                'zostały skopiowane z oryginalnego źródła: <a href="http://sio.'
                'men.gov.pl/index.php/pomoc/faqs">http://sio.men.gov.pl/index.php'
                '/pomoc/faqs</a></strong></p>'
            )
            o.write(bs)
        print('* Processing: %s...' % file)
