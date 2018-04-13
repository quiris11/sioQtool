#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#


def get_regions_reports():
    import os
    try:
        from urllib.request import build_opener
    except ImportError:
        from urllib2 import build_opener

    try:
        from urllib.request import HTTPCookieProcessor
    except ImportError:
        from urllib2 import HTTPCookieProcessor

    home = os.path.expanduser("~")

    report_list = [
        ['26', 'dolnoslaskie'],
        ['27', 'kujawsko-pomorskie'],
        ['28', 'lubelskie'],
        ['29', 'lubuskie'],
        ['30', 'lodzkie'],
        ['31', 'malopolskie'],
        ['32', 'mazowieckie'],
        ['33', 'opolskie'],
        ['34', 'podkarpackie'],
        ['35', 'podlaskie'],
        ['36', 'pomorskie'],
        ['37', 'slaskie'],
        ['38', 'swietokrzyskie'],
        ['39', 'warminsko-mazurskie'],
        ['40', 'wielkopolskie'],
        ['41', 'zachodniopomorskie'],
    ]

    opener = build_opener(HTTPCookieProcessor())

    for i in report_list:
        print('* Downloading: ' + i[1])
        url = (
            'https://raporty-sio2.men.gov.pl/raports/getraport?'
            'idPodmiot=' + i[0] + '&idRaport=1'
        )
        page = opener.open(url)
        with open(
                os.path.join(home, 'NSIO', 'woj_' + i[1] + '.xls'), 'w') as f:
                f.write(page.read())


def get_reports(force):
    import os
    import shutil
    from lxml import etree
    try:
        from urllib.request import build_opener
    except ImportError:
        from urllib2 import build_opener

    try:
        from urllib.request import HTTPCookieProcessor
    except ImportError:
        from urllib2 import HTTPCookieProcessor

    XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
             'x': 'urn:schemas-microsoft-com:office:excel',
             'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
    home = os.path.expanduser("~")

    report_list = [
        ['1', 'rspo_aktywne2.xls'],
        ['2', 'ee_przedszk2.xls'],
        ['3', 'ee_sp2.xls'],
        ['6', 'zawody2.xls'],
        ['7', 'rspo_nieaktywne2.xls'],
        ['27', 'licz_ucz_oddz_wg_klas2.xls']
    ]

    opener = build_opener(HTTPCookieProcessor())

    print('* Downloading reports...')
    for i in report_list:
        try:
            tree = etree.parse(os.path.join('%s/NSIO/%s' % (home, i[1])))
            title_old = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                   namespaces=XLSNS)[0]
        except BaseException:
            print('Error! Incorrect file: %s/NSIO/%s' % (home, i[1]))
            title_old = ''
        url = (
            'https://raporty-sio2.men.gov.pl/raports/getraport?'
            'idPodmiot=38&idRaport=' + i[0]
        )
        page = opener.open(url)
        with open(os.path.join(home, 'NSIO', 'new_' + i[1]), 'wb') as f:
            f.write(page.read())
        try:
            tree = etree.parse(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
            title_new = tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                   namespaces=XLSNS)[0]
        except BaseException:
            print('Error! Incorrect file: %s/NSIO/new_%s' % (home, i[1]))
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
            continue
        print('Local file title:  ' + title_old)
        print('Remote file title: ' + title_new)
        if title_old == title_new and not force:
            print('* NOT updated. Same report already downloaded...')
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))
        else:
            print('* Remote file: %s/NSIO/new_%s updated.\n'
                  '* Replacing the old one...' % (home, i[1]))
            shutil.copyfile(os.path.join('%s/NSIO/new_%s' % (home, i[1])),
                            os.path.join('%s/NSIO/%s' % (home, i[1])))
            os.remove(os.path.join('%s/NSIO/new_%s' % (home, i[1])))


if __name__ == "__main__":
    get_regions_reports()
