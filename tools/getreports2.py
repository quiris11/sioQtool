#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#


def get_reports():
    import os
    import shutil
    from lxml import etree
    import urllib2

    XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
             'x': 'urn:schemas-microsoft-com:office:excel',
             'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
    home = os.path.expanduser("~")

    report_list = [
        ['1', 'rspo_aktywne.xls'],
        ['2', 'ee_przedszk.xls'],
        ['3', 'ee_sp.xls'],
        ['4', 'obwody_sp.xls'],
        ['5', 'obwody_gm.xls'],
        ['6', 'zawody.xls'],
        ['7', 'rspo_nieaktywne.xls']
    ]

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    print('* Downloading reports...')
    for i in report_list:
        try:
            tree = etree.parse(os.path.join('%s/NSIO/%s' % (home, i[1])))
            title_old = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                   namespaces=XLSNS)[0]
        except:
            print('Error! Incorrect file: %s/NSIO/%s' % (home, i[1]))
            continue
        url = (
            'https://bezpieczenstwo-formularz.men.gov.pl/frame/sdz/raporty/'
            'raport/idPodmiot/38/idRaport/' + i[0]
        )
        page = opener.open(url)
        with open(os.path.join(home, 'NSIO', 'new_' + i[1]), 'w') as f:
            f.write(page.read())
        try:
            tree = etree.parse(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
            title_new = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                   namespaces=XLSNS)[0]
        except:
            print('Error! Incorrect file: %s/NSIO/new_%s' % (home, i[1]))
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
            continue
        print('Local file title:  ' + title_old)
        print('Remote file title: ' + title_new)
        if title_old == title_new:
            print('* NOT updated. Same report already downloaded...')
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
        else:
            print('* Remote file: %s/NSIO/new_%s upadated.\n'
                  '* Replacing the old one...' % (home, i[1]))
            shutil.copyfile(os.path.join('%s/NSIO/new_%s' % (home, i[1])),
                            os.path.join('%s/NSIO/%s' % (home, i[1])))
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
