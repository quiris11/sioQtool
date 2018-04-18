#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

from __future__ import print_function
from lxml import etree
from collections import Counter
from datetime import datetime
from dictionaries import kat_ucz_dict
from dictionaries import publ_dict
from dictionaries import type_dict
from dictionaries import specyfika_dict
from dictionaries import zawod_dict
from dictionaries import typ_organu_prow_dict
from dictionaries import jst_dict
from tools.getreports2 import get_reports
from tools.getfaqs import get_faqs
from tools.transform import transform
from xlsxwriter.workbook import Workbook
import unicodedata
import argparse
import os
import csv
import difflib
import glob
import shutil
import sys
import time


home = os.path.expanduser("~")
XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}
XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
         'x': 'urn:schemas-microsoft-com:office:excel',
         'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

BORDER_DATE = datetime.strptime('2018-03-31', '%Y-%m-%d')
BORDER_DATEZ = datetime.strptime('2017-09-01', '%Y-%m-%d')

parser = argparse.ArgumentParser()
parser.add_argument('oldpath', nargs='?', default=os.path.join(home, 'OSIO'),
                    help='path to DIR with old SIO XML files '
                         '(default: ~/OSIO)')
parser.add_argument('newpath', nargs='?', default=os.path.join(home, 'NSIO'),
                    help='path to DIR with new SIO XLS files '
                         '(default: ~/NSIO)')
parser.add_argument('-e', '--exp',
                    help='OSIO: unpack EXP files in oldpath '
                         '(required: Dkod tool)',
                    action="store_true")
parser.add_argument('-t', '--ns-mail-tough-check',
                    help='NSIO: e-mails tough checking',
                    action="store_true")
parser.add_argument("--move",
                    help="move reports/FAQs to 'src' directory",
                    action="store_true")
parser.add_argument("-c", "--compare",
                    help="compare new reports/FAQs with old reports/FAQs",
                    action="store_true")
parser.add_argument('--get-reports',
                    help="get new NSIO reports from SIO portal",
                    action="store_true")
parser.add_argument('--get-faqs',
                    help="get FAQs from SIO portal",
                    action="store_true")
parser.add_argument('-n', '--skip-new-overwrite',
                    help="skip overwriting new SIO temporary lists",
                    action="store_true")
parser.add_argument('-s', '--skip-old-overwrite',
                    help="skip overwriting old SIO temporary lists",
                    action="store_true")
parser.add_argument('-f', '--force',
                    help="force downloading new reports",
                    action="store_true")
args = parser.parse_args()


def compare_csvs(sio_report_list):
    for item in sio_report_list:
        print('*** ' + item[1] + ' ***')
        try:
            with open(os.path.join(item[2], 'src', item[1]), 'r') as f:
                lines1 = f.read().split('\n')
            with open(os.path.join(item[2], item[1]), 'r') as f:
                lines2 = f.read().split('\n')
                for line in difflib.unified_diff(
                    lines1, lines2,
                    fromfile='stary: ' + item[2] + '/src/' + item[1],
                    tofile='nowy: ' + item[2] + '/' + item[1],
                    lineterm='', n=0
                ):
                        print(line)
        except IOError:
            print('* Error')
            continue
        print('* OK')


sio_report_list = ([
    ['EE SP: ponizej zero', 'etapy_eduk_szk_podst_ponizej_zero.csv',
     '!critical!'],
    ['EE SP: zero', 'etapy_eduk_szk_podst_zero.csv', '!critical!'],
    ['EE P: ponizej zero',
     'etapy_eduk_przedszk_i_inne_formy_ponizej_zero.csv', '!critical!'],
    ['EE P: zero', 'etapy_eduk_przedszk_i_inne_formy_zero.csv', '!critical!'],
    ['EE SP: pierwszy etap', 'etapy_eduk_szk_podst_pierwszy_etap.csv',
     '!critical!'],
    ['EE SP: drugi etap', 'etapy_eduk_szk_podst_drugi_etap.csv', '!critical!'],
    ['OS: all items', 'os_all_items.csv', '!normal!'],
    ['OS: duplicated REGONs', 'os_zdublowane_regony.csv', '!critical!'],
    ['OS: duplicated RSPOs', 'os_zdublowane_rspo.csv', '!critical!'],
    # ['OS: no RSPOs', 'os_brak_nr_rspo.csv', '!critical!'],
    # ['OS: no e-mails', 'os_brak_adresu_email.csv', '!critical!'],
    ['OS: incorrect RSPOs', 'os_niepoprawne_numery_rspo.csv', '!critical!'],
    ['OS: incorrect REGONSs', 'os_niepoprawne_numery_regon.csv', '!critical!'],
    ['OS: incorrect publicznosc', 'osn_niepoprawne_pole_publicznosc.csv',
        '!critical!'],
    ['OS: incorrect kategoria uczniow',
        'osn_niepoprawne_pole_kategoria_uczniow.csv', '!critical!'],
    ['NS: all items', 'ns_all_items.csv', '!normal!'],
    ['NS: Missing REGONs in old SIO existing in a new SIO\n  with birthdate '
        'earlier than %s' % BORDER_DATE,
     'osn_brakujace_w_starym_sio_numery_regon_z_nowego_sio.csv', '!critical!'],
    ['OS: Terminated items existing in old SIO (REGON checked)'
        '\n  with termination date older than %s' % BORDER_DATEZ,
     'osn_nieistniejace_szkoly_wykazane_w_starym_sio.csv', '!critical!'],
    ['OS: incorrect type', 'osn_niepoprawne_pole_typ.csv', '!critical!'],
    ['OS: incorrect specyfika', 'osn_niepoprawne_pole_specyfika.csv',
        '!critical!'],
    ['OS: incorrect typ organu', 'osn_niezgodny_typ_organu_prow.csv',
        '!critical!'],
    ['OS: different jobs',
        'osn_nieznalezione_w_nowym_sio_zawody_wykazane_w_starym_sio.csv',
        '!critical!'],
    ['OS: different REGONs',
        'osn_niezgodne_numery_regon.csv',
        '!critical!'],
    ['NS: incorrect szkolaObwodowa',
        'osn_niezgodne_dane_o_obwodowosci.csv',
        '!critical!'],
    ['NS: different e-mails', 'osn_rozne_adresy_email.csv', '!critical!'],
    ['NS: different phones', 'osn_rozne_nr_telefonu.csv', '!critical!'],
    # turned off - impossible to correct such differences
    # ['NS: different jst e-mails', 'osn_rozne_jst_email.csv', '!critical!'],
    # ['NS: different jst phones', 'osn_rozne_jst_telefon.csv', '!critical!'],
    ['NS: missing ZEAS in old SIO', 'osn_brakujace_zeasy_stare_sio.csv',
        '!critical!'],
    ['NS: missing ZEAS in new SIO', 'osn_brakujace_zeasy_nowe_sio.csv',
        '!critical!'],
    ['NS: different dormitories', 'osn_rozne_internaty.csv', '!critical!'],
    ['NS: problematic JST REGONs', 'osn_jst_problematyczne_numery_regon.csv',
        '!critical!'],
    ['NS: different or missing parent',
        'osn_brak_lub_niezgodny_org_nadrzedny.csv',
        '!critical!'],
    ['NS: incorrect name of „branżówka” school',
        'osn_nieskorygowana_nazwa_branzowki.csv',
        '!critical!'],
    ['NS: problem with item names',
        'osn_niezgodne_nazwy_jednostek.csv',
        '!critical!'],
    ['NS: no students in new SIO',
        'ns_brak_przypisanych_uczniow.csv',
        '!critical!'],
    ['ALL: all problems', 'all.csv', '!critical!']
])

header_list = [
    'RSPO',
    'REGON',
    'powiat',
    'gmina',
    'typ',
    'publicz.',
    'kat. ucz.',
    'nazwa',
    'email',
    'telefon',
    'miejscowosc',
    'ulica',
    'nr',
    'kod',
    'poczta',
    'organ prow',
    'kod woj. org. wyd.',
    'kod pow. org. wyd.',
    'kod gm. org. wyd.',
    'email kom.',
    'specyfika',
    'typ organu prow',
    'czy obwodowa?',
    'ID organu scalającego'
]


def get_os_internaty(tree):
    rows = []
    inter_tags = tree.xpath('//internat', namespaces=XSNS)
    if inter_tags is None:
        return None
    for it in inter_tags:
        if it.get('numerIdent') is not None:
            itree = etree.ElementTree(it.getparent())
            numerIdent = itree.xpath('//identyfikacja',
                                     namespaces=XSNS)[0].get('numerIdent')
            if numerIdent is None:
                continue
            try:
                nrRspo = int(tree.xpath(
                    '//identyfikacja[@numerIdent="' + numerIdent + '"]/i2c',
                    namespaces=XSNS
                )[0].get('nrRspo'))
            except BaseException:
                nrRspo = 0
            rows.append(nrRspo)
    return rows


def get_ns_zawody(path):
    tree = etree.parse(os.path.join(path, 'zawody2.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    ns_rspos = []
    ns_zawody = []
    # skipped first two title cells
    for i in tree.xpath('//ss:Row/ss:Cell[1]/ss:Data/text()',
                        namespaces=XLSNS)[2:]:
        ns_rspos.append(xs(i))
    for i in tree.xpath('//ss:Row/ss:Cell[5]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_zawody.append(xs(i))
    data = zip(ns_rspos, ns_zawody)
    return data


def get_os_zawody(tree):
    rows = []
    zawody_tags = tree.xpath('//zawody', namespaces=XSNS)
    if zawody_tags is None:
        return None
    for zt in zawody_tags:
        parent = zt.getparent()
        numerIdent = parent.get('numerIdent')
        if numerIdent is None:
            continue
        try:
            nrRspo = int(tree.xpath(
                '//identyfikacja[@numerIdent="' + numerIdent + '"]/i2c',
                namespaces=XSNS
            )[0].get('nrRspo'))
        except BaseException:
            nrRspo = 0
        ztree = etree.ElementTree(zt)
        zs = ztree.xpath('//zawod', namespaces=XSNS)
        for z in zs:
            rows.append([nrRspo, int(z.get('idZawodu'))])
    return rows


def duplicated_list(mylist):
    return [k for k, v in Counter(mylist).items() if v > 1]


def xs(s):
    if s is None:
        return ''
    try:
        return unicode(s.strip()).encode('utf8')
    except NameError:
        return s.strip()


def xi(s):
    if s is None:
        return 0
    return int(s)


def os_row(i, a, scalid, rspo_nad, regon_nad, name_nad, parent_tag):
    lista = [
        xi(i.get('nrRspo')),
        xs(i.get('regon')),
        xs(i.get('pow')),
        xs(i.get('gm')),
        xi(i.get('typJed')),
        xi(i.get('publicznosc')),
        xi(i.get('kategoriaUczniow')),
        xs(i.get('nazwa')),
        xs(a.get('email')),
        xs(a.get('telefon')),
        xs(a.get('nazwaMiejsc')),
        xs(a.get('ulica')),
        xs(a.get('nrDomu')),
        xs(a.get('kodPoczt')),
        xs(a.get('poczta')),
        xs(i.get('nazwaOrganuProw')),
        xs(i.get('orgWydWoj')),
        xs(i.get('orgWydPow')),
        xs(i.get('orgWydGm')),
        xs(a.get('emailKomorki')),
        xi(i.get('specyfikaSzkoly')),
        xi(i.get('typOrganuProw')),
        xs(i.get('szkolaObwodowa')),
        xs(scalid),
        xi(rspo_nad),
        xs(regon_nad),
        xs(name_nad),
        xs(parent_tag),
        xs(i.get('imiePat'))
    ]
    print(xs(i.get('imiePat')))
    return lista


def get_os_12_row(tree, scalid):
    def get_l_ucz(wiersz):
        try:
            li = int(wiersz.get('kol2'))
        except BaseException:
            li = 0
        return li
    file_rows = []
    for typ in ('szkolaPodst', 'filiaSzkolyPodst'):
        ids = tree.xpath('//' + typ + '/identyfikacja', namespaces=XSNS)
        for i in ids:
            l1 = l2 = l3 = l4 = l5 = l6 = 0
            try:
                nrRspo = int(tree.xpath(
                    '//' + typ + '/identyfikacja[@numerIdent="' +
                    i.get('numerIdent') +
                    '"]/i2c',
                    namespaces=XSNS)[0].get('nrRspo'))
            except BaseException:
                nrRspo = 0
            u31s = tree.xpath(
                '//' + typ + '/uczniowieSzkolyPodst/'
                'oddzialy[@numerIdent="' +
                i.get('numerIdent') +
                '"]//wierszU3_1',
                namespaces=XSNS)
            for u in u31s:
                if u.get('kol0') == '4':
                    l1 += get_l_ucz(u)
                elif u.get('kol0') == '5':
                    l2 += get_l_ucz(u)
                elif u.get('kol0') == '6':
                    l3 += get_l_ucz(u)
                elif u.get('kol0') == '7':
                    l4 += get_l_ucz(u)
                elif u.get('kol0') == '8':
                    l5 += get_l_ucz(u)
                elif u.get('kol0') == '9':
                    l6 += get_l_ucz(u)
            file_rows.append([nrRspo, l1, l2, l3, l4, l5, l6, scalid])
    return file_rows


def get_os_ee_row(tree, scalid):
    file_rows = []
    for typ in ('szkolaPodst', 'filiaSzkolyPodst'):
        ids = tree.xpath('//' + typ + '/identyfikacja', namespaces=XSNS)
        for i in ids:
            try:
                nrRspo = int(tree.xpath(
                    '//' + typ + '/identyfikacja[@numerIdent="' +
                    i.get('numerIdent') +
                    '"]/i2c',
                    namespaces=XSNS)[0].get('nrRspo'))
            except BaseException:
                nrRspo = 0
            u331s = tree.xpath(
                '//' + typ + '/uczniowieSzkolyPodst/'
                'oddzialyPrzedszkolne[@numerIdent="' +
                i.get('numerIdent')[:-1] + '1' +
                '"]/dzieciWgOddzialow/u3_3/u3_3_1',
                namespaces=XSNS)
            u332s = tree.xpath(
                '//' + typ + '/uczniowieSzkolyPodst/'
                'oddzialyPrzedszkolne[@numerIdent="' +
                i.get('numerIdent')[:-1] + '1' +
                '"]/dzieciWgOddzialow/u3_3/u3_3_2',
                namespaces=XSNS)
            for u in u331s:
                try:
                    l_ucz_pon_zero = int(u.get('kol2'))
                except BaseException:
                    l_ucz_pon_zero = 0
                try:
                    l_ucz_zero = int(u332s[u331s.index(u)].get('kol2'))
                except BaseException:
                    l_ucz_zero = 0
                file_rows.append([nrRspo, l_ucz_pon_zero, l_ucz_zero,
                                 scalid])
    for typ in ('punktPrzedszkolny',
                'zespolWychowaniaPrzedszkolnego',
                'przedszkole'):
        typels = tree.xpath('//' + typ, namespaces=XSNS)
        for t in typels:
            ttree = etree.ElementTree(t)
            try:
                nrRspo = int(ttree.xpath('//identyfikacja/i2c',
                             namespaces=XSNS)[0].get('nrRspo'))
            except BaseException:
                nrRspo = 0
            u331p = ttree.xpath(
                '//dzieciWgOddzialow/u3_3/u3_3_1',
                namespaces=XSNS)
            u332p = ttree.xpath(
                '//dzieciWgOddzialow/u3_3/u3_3_2',
                namespaces=XSNS)
            for u in u331p:
                try:
                    l_ucz_pon_zero = int(u.get('kol2'))
                except BaseException:
                    l_ucz_pon_zero = 0
                try:
                    l_ucz_zero = int(u332p[u331p.index(u)].get('kol2'))
                except BaseException:
                    l_ucz_zero = 0
                file_rows.append([nrRspo, l_ucz_pon_zero, l_ucz_zero,
                                 scalid])
    return file_rows


def get_jst_row(tree):
    jst_row = []
    i2b = tree.xpath('//i2b', namespaces=XSNS)
    for i in i2b:
        if i.get('typJed') == '103':
            jst_row.append([
                i.getparent().get('numerIdent'),
                jst_dict[
                    int(
                        xs(i.get('wojJST')) +
                        xs(i.get('powJST')) +
                        xs(i.get('gmJST'))
                    )]
            ])
    return jst_row


def get_os_row(tree, scalid):
    file_rows = []
    i2as = tree.xpath('//i2a', namespaces=XSNS)
    if len(i2as) > 0:
        rspo_nad = 0 if i2as[0].get(
            'nrRspo') is None else i2as[0].get('nrRspo')
        regon_nad = i2as[0].get('regon')
        nazwa_nad = i2as[0].get('nazwa')
    else:
        rspo_nad = '0'
        regon_nad = ''
        nazwa_nad = ''
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        file_rows.append(os_row(
            i, a, scalid,
            '0' if i.get('nrRspo') == rspo_nad else rspo_nad,
            '' if i.get('nrRspo') == rspo_nad else regon_nad,
            '' if i.get('nrRspo') == rspo_nad else nazwa_nad,
            i.getparent().getparent().tag))
    return file_rows


def get_os_data(path):
    data = []
    jsts = [['OSIO', 26]]
    os_zawody = []
    os_ee_data = []
    os_12_data = []
    os_internaty = []
    for root, dirs, files in os.walk(path):
        for single_file in files:
            if single_file.endswith('.xml'):
                if 'jednostkiScalone' in root:
                    scalid = '/'.join(root.split('/')[-2:-1])
                else:
                    scalid = '/'.join(root.split('/')[-1:])
                single_file_path = os.path.join(root, single_file)
                single_file_tree = etree.parse(single_file_path)
                data = data + get_os_row(single_file_tree, scalid)
                jsts = jsts + get_jst_row(single_file_tree)
                os_ee_data = os_ee_data + get_os_ee_row(single_file_tree,
                                                        scalid)
                os_12_data = os_12_data + get_os_12_row(single_file_tree,
                                                        scalid)
                os_internaty = os_internaty + get_os_internaty(
                    single_file_tree)
                if get_os_zawody(single_file_tree) != []:
                    for r in get_os_zawody(single_file_tree):
                        os_zawody.append(r)
    jsts_dict = dict(jsts)
    jst_dict_rew = dict((r[1], r[0]) for r in jsts)
    return(data, os_zawody, jsts_dict, jst_dict_rew, os_ee_data, os_12_data,
           os_internaty)


def get_terminated(tree):
    regons = []
    term_d = []
    rspos = []
    for i in tree.xpath('//ss:Row', namespaces=XLSNS)[3:]:
        rtree = etree.ElementTree(i)
        cd = rtree.xpath('//ss:Cell/ss:Data', namespaces=XLSNS)
        if cd[0].text is None:
            continue
        else:
            regons.append(xs(cd[9].text))
            term_d.append(xs(cd[4].text))
            rspos.append(xs(cd[0].text))
    return zip(regons, term_d, rspos)


def get_ns_ee_data(path, typ):
    tree = etree.parse(os.path.join(path, 'ee_' + typ + '2.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    dataee = []
    ns_rspos = []
    ns_regons = []
    ns_typs = []
    ns_names = []
    ns_org_rej = []
    ns_datas_rozp_dzial = []
    ns_emails = []
    ns_tels = []
    ns_publicznosc = []
    ns_kat_uczn = []
    ns_ee_pzero = []
    ns_ee_zero = []
    ns_ee_first = []
    ns_ee_second = []
    ns_ee_irrelevant = []

    for i in tree.xpath('//ss:Row', namespaces=XLSNS)[2:]:
        rtree = etree.ElementTree(i)
        cd = rtree.xpath('//ss:Cell/ss:Data', namespaces=XLSNS)
        try:
            ns_rspos.append(xi(cd[0].text))
        except BaseException:
            ns_rspos.append(xs(cd[0].text))
        ns_typs.append(xs(cd[2].text))
        ns_names.append(xs(cd[3].text))
        if cd[4].text is None:
            ns_ee_pzero.append('.')
        else:
            ns_ee_pzero.append(xs(cd[4].text))
        if cd[5].text is None:
            ns_ee_zero.append('.')
        else:
            ns_ee_zero.append(xs(cd[5].text))
        if cd[6].text is None:
            ns_ee_first.append('.')
        else:
            ns_ee_first.append(xs(cd[6].text))
        if cd[7].text is None:
            ns_ee_second.append('.')
        else:
            ns_ee_second.append(xs(cd[7].text))
        if cd[8].text is None:
            ns_ee_irrelevant.append('.')
        else:
            ns_ee_irrelevant.append(xs(cd[8].text))
        ns_regons.append(xs(cd[13].text))
        ns_org_rej.append(xs(cd[10].text))
        ns_datas_rozp_dzial.append(xs(cd[33].text))
        ns_publicznosc.append(xs(cd[30].text))
        ns_kat_uczn.append(xs(cd[29].text))
        if cd[25].text is None:
            ns_emails.append('')
        else:
            ns_emails.append(cd[25].text)
        if cd[24].text is None:
            ns_tels.append('')
        else:
            ns_tels.append(cd[24].text)
    dataee = zip(ns_rspos, ns_regons, ns_org_rej, ns_names, ns_typs, ns_emails,
                 ns_tels, ns_datas_rozp_dzial, ns_publicznosc, ns_kat_uczn,
                 ns_ee_pzero, ns_ee_zero, ns_ee_first, ns_ee_second,
                 ns_ee_irrelevant)
    return dataee


def get_jst_data(path):
    tree = etree.parse(os.path.join(path, 'rspo_aktywne2.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    ns_regons = []
    ns_type_ids = []
    ns_typs = []
    ns_names = []
    ns_emails = []
    ns_tels = []
    ns_org_rej = []
    for i in tree.xpath('//ss:Row', namespaces=XLSNS)[2:]:
        rtree = etree.ElementTree(i)
        cd = rtree.xpath('//ss:Cell/ss:Data', namespaces=XLSNS)
        if (cd[1].text == '130' or
            cd[1].text == '131' or
            cd[1].text == '132' or
            cd[1].text == '133' or
                cd[1].text == '160'):
            ns_type_ids.append(xi(cd[1].text))
            ns_typs.append(xs(cd[2].text))
            ns_names.append(xs(cd[3].text))
            ns_regons.append(xs(cd[8].text))
            if cd[21].text is None:
                ns_emails.append('')
            else:
                ns_emails.append(xs(cd[21].text))
            if cd[20].text is None:
                ns_tels.append('')
            else:
                ns_tels.append(xs(cd[20].text))
            ns_org_rej.append(xs(cd[5].text))
    data = zip(ns_type_ids, ns_typs, ns_names, ns_regons, ns_emails, ns_tels,
               ns_org_rej)
    return data


def get_ns_liczba_uczniow_oddzialow(path):
    tree = etree.parse(os.path.join(path, 'licz_ucz_oddz_wg_klas2.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    ns_rspos = []
    ns_licz_uczniow = []
    ns_licz_oddzialow = []

    for i in tree.xpath('//ss:Row', namespaces=XLSNS)[2:]:
        rtree = etree.ElementTree(i)
        cd = rtree.xpath('//ss:Cell/ss:Data', namespaces=XLSNS)
        if cd[0].text is None:
                continue
        else:
            try:
                ns_rspos.append(xi(cd[0].text))
            except BaseException:
                ns_rspos.append(xs(cd[0].text))
            try:
                ns_licz_uczniow.append(xi(cd[5].text))
            except BaseException:
                ns_licz_uczniow.append(xs(cd[5].text))
            try:
                ns_licz_oddzialow.append(xi(cd[6].text))
            except BaseException:
                ns_licz_oddzialow.append(xs(cd[6].text))
    data = zip(ns_rspos, ns_licz_uczniow, ns_licz_oddzialow)
    return data


def get_ns_data(path):
    tree = etree.parse(os.path.join(path, 'rspo_aktywne2.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    ns_rspos = []
    ns_regons = []
    ns_typs = []
    ns_names = []
    ns_org_rej = []
    ns_datas_rozp_dzial = []
    ns_emails = []
    ns_tels = []
    ns_publicznosc = []
    ns_kat_uczn = []
    ns_specyfika = []
    ns_typ_org_prow = []
    ns_org_prow = []
    ns_czesc_miejska = []
    ns_internaty = []
    ns_rspos_nad = []
    ns_names_nad = []
    ns_obwodowa = []
    ns_typ_id = []
    for i in tree.xpath('//ss:Row', namespaces=XLSNS)[2:]:
        rtree = etree.ElementTree(i)
        cd = rtree.xpath('//ss:Cell/ss:Data', namespaces=XLSNS)
        if cd[0].text is None:
                continue
        else:
            try:
                ns_rspos.append(xi(cd[0].text))
            except BaseException:
                ns_rspos.append(xs(cd[0].text))
            ns_regons.append(xs(cd[8].text))
            ns_typs.append(xs(cd[2].text))
            ns_names.append(xs(cd[3].text))
            ns_org_rej.append(xs(cd[5].text))
            ns_datas_rozp_dzial.append(xs(cd[33].text))
            ns_publicznosc.append(xs(cd[26].text))
            if cd[25].text is None:
                ns_kat_uczn.append('Bez kategorii')
            else:
                ns_kat_uczn.append(xs(cd[25].text))
            if cd[21].text is None:
                ns_emails.append('')
            else:
                ns_emails.append(cd[21].text)
            if cd[20].text is None:
                ns_tels.append('')
            else:
                ns_tels.append(cd[20].text)
            if cd[24].text is None:
                ns_specyfika.append('brak specyfiki')
            else:
                ns_specyfika.append(xs(cd[24].text))
            ns_typ_org_prow.append(xs(cd[6].text))
            ns_org_prow.append(xs(cd[7].text))
            ns_czesc_miejska.append(xs(cd[23].text))
            try:
                ns_internaty.append(xi(cd[43].text))
            except BaseException:
                ns_internaty.append(xs(cd[43].text))
            if cd[38].text is None:
                ns_rspos_nad.append(0)
            else:
                try:
                    ns_rspos_nad.append(xi(cd[38].text))
                except BaseException:
                    ns_rspos_nad.append(xs(cd[38].text))
            if cd[40].text is None:
                ns_names_nad.append('')
            else:
                ns_names_nad.append(xs(cd[40].text))
            try:
                ns_obwodowa.append(xi(cd[44].text))
            except BaseException:
                ns_obwodowa.append(xs(cd[44].text))
            if cd[1].text is None:
                ns_typ_id.append(0)
            else:
                try:
                    ns_typ_id.append(xi(cd[1].text))
                except BaseException:
                    ns_typ_id.append(xs(cd[1].text))

    data = zip(ns_rspos, ns_regons, ns_org_rej, ns_names, ns_typs, ns_emails,
               ns_tels, ns_datas_rozp_dzial, ns_publicznosc, ns_kat_uczn,
               ns_specyfika, ns_typ_org_prow, ns_org_prow, ns_czesc_miejska,
               ns_internaty, ns_rspos_nad, ns_names_nad, ns_obwodowa, ns_typ_id
               )
    return data


def load_exceptions():
    li = []
    try:
        with open(os.path.join(args.newpath, 'exceptions.csv')) as f:
            csvread = csv.reader(f, delimiter=';', quotechar='"',
                                 quoting=csv.QUOTE_NONNUMERIC)
            for r in csvread:
                if r[0] == 'missregon':
                    li.append(r[1])
    except BaseException:
        pass
    return li


def generate_jst_reports():
    print('* Generating JST report files...')
    with open(os.path.join('!critical!', 'temp.csv'), 'w') as outfile:
        for item in sio_report_list:
            if item[2] == '!critical!':
                with open(os.path.join(item[2], item[1])) as infile:
                    for line in infile:
                        outfile.write(line)
    li = [
        'ID organu scalającego: ',
        'Organ scalający: ',
        'Opis problemu: ',
        'Stare SIO: ',
        'Nowe SIO: ',
        'Nr RSPO: ',
        'REGON: ',
        'Typ jednostki: ',
        'Nazwa jednostki: ',
        'E-mail: ',
        'Telefon: '
    ]

    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize(
            'NFKD', text) if unicodedata.category(c) != 'Mn')

    with open(os.path.join('!critical!', 'temp.csv')) as f:
        csvread = csv.reader(f, delimiter=';', quotechar='"',
                             quoting=csv.QUOTE_NONNUMERIC)
        with open(os.path.join('!critical!', 'all.csv'), 'w') as o:
            csvwrite = csv.writer(o, delimiter=';', quotechar='"',
                                  quoting=csv.QUOTE_NONNUMERIC)
            csvwrite.writerow([
                'ID organu scalającego',
                'Organ scalający',
                'Opis problemu',
                'Stare SIO',
                'Nowe SIO',
                'Nr RSPO',
                'REGON',
                'Typ jednostki',
                'Nazwa jednostki',
                'E-mail',
                'Telefon'
            ])
            if os.path.exists(os.path.join('!critical!', 'JST2')):
                shutil.rmtree(os.path.join('!critical!', 'JST2'))
                os.makedirs(os.path.join('!critical!', 'JST2'))
            else:
                os.makedirs(os.path.join('!critical!', 'JST2'))
            for r in csvread:
                for i, x in enumerate(r):
                    if type(x) is float:
                        r[i] = int(x)
                if r[6] == 'REGON':
                    continue
                else:
                    csvwrite.writerow(r)
                    try:
                        nfname = strip_accents(r[1].decode('utf8'))
                    except AttributeError:
                        nfname = strip_accents(r[1])
                    nfname = nfname.replace(u'\u2013', '-').replace('/', '')\
                                   .replace(':', '_').replace(u'\u0142', 'l')\
                                   .replace(u'\u0141', 'L')
                    nfname = "".join(x for x in nfname if (
                        x.isalnum() or x.isspace() or x in ('_', '-', '.')))
                    with open(
                        os.path.join(
                            '!critical!',
                            'JST2',
                            '%s (%s).txt' % (nfname, r[0])), 'a') as j:
                        csv.writer(j, delimiter='\n', quotechar="'",
                                   lineterminator='\n\n\n',
                                   quoting=csv.QUOTE_MINIMAL).writerow([
                                       li[0] + str(r[0]),
                                       li[1] + str(r[1]),
                                       li[2] + str(r[2]),
                                       li[3] + str(r[3]),
                                       li[4] + str(r[4]),
                                       li[5] + str(r[5]),
                                       li[6] + str(r[6]),
                                       li[7] + str(r[7]),
                                       li[8] + str(r[8]),
                                       li[9] + str(r[9]),
                                       li[10] + str(r[10])])
    os.remove(os.path.join('!critical!', 'temp.csv'))


start = time.clock()
if args.oldpath.endswith('.krt'):
    print('Extracting KRT file...')
    transform(args.oldpath, '.krt')
    oldpath = 'OSIO'
elif args.exp:
    print('Extracting EXP files...')
    transform(args.oldpath, '.exp')
    oldpath = 'OSIO'
else:
    oldpath = args.oldpath

if args.get_faqs:
    get_faqs(args.move, args.compare)
    sys.exit()

if args.get_reports:
    get_reports(args.force)
    sys.exit()

if args.move:
    print('* Moving new reports to src directory...')
    for item in sio_report_list:
        if not os.path.exists(os.path.join(item[2], 'src')):
            os.makedirs(os.path.join(item[2], 'src'))
        try:
            shutil.copyfile(os.path.join(item[2], item[1]),
                            os.path.join(item[2], 'src', item[1]))
        except IOError:
            continue
    sys.exit()

if args.compare:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('* Comparing new reports with old reports...')
    compare_csvs(sio_report_list)
    sys.exit()

if not os.path.exists(os.path.join('!normal!')):
    os.makedirs(os.path.join('!normal!'))
if not os.path.exists(os.path.join('!critical!')):
    os.makedirs(os.path.join('!critical!'))

missregons = load_exceptions()
if not args.skip_new_overwrite:
    print('! Preparing new SIO data from source files...')
    ns_data_list = get_ns_data(args.newpath)
    ns_l_ucz_oddz = get_ns_liczba_uczniow_oddzialow(args.newpath)
    ns_jst_list = get_jst_data(args.newpath)
    ns_ee_sp_list = get_ns_ee_data(os.path.join(args.newpath), 'sp')
    ns_ee_p_list = get_ns_ee_data(os.path.join(args.newpath), 'przedszk')
    ns_zawody_list = get_ns_zawody(args.newpath)
    term_tree = etree.parse(os.path.join(args.newpath, 'rspo_nieaktywne2.xls'))
    print('* ' + term_tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                 namespaces=XLSNS)[0])
    ns_term_list = get_terminated(term_tree)
    with open(os.path.join(args.newpath, 'ns_data_list.txt'), 'w') as f:
        f.write(str(ns_data_list))
    with open(os.path.join(args.newpath, 'ns_l_ucz_oddz.txt'), 'w') as f:
        f.write(str(ns_l_ucz_oddz))
    with open(os.path.join(args.newpath, 'ns_jst_list.txt'), 'w') as f:
        f.write(str(ns_jst_list))
    with open(os.path.join(args.newpath, 'ns_ee_sp_list.txt'), 'w') as f:
        f.write(str(ns_ee_sp_list))
    with open(os.path.join(args.newpath, 'ns_ee_p_list.txt'), 'w') as f:
        f.write(str(ns_ee_p_list))
    with open(os.path.join(args.newpath, 'ns_zawody_list.txt'), 'w') as f:
        f.write(str(ns_zawody_list))
    with open(os.path.join(args.newpath, 'ns_term_list.txt'), 'w') as f:
        f.write(str(ns_term_list))
else:
    print('* Loading prepared new SIO data from txt files...')
    with open(os.path.join(args.newpath, 'ns_data_list.txt'), 'r') as f:
        ns_data_list = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_l_ucz_oddz.txt'), 'r') as f:
        ns_l_ucz_oddz = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_jst_list.txt'), 'r') as f:
        ns_jst_list = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_ee_sp_list.txt'), 'r') as f:
        ns_ee_sp_list = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_ee_p_list.txt'), 'r') as f:
        ns_ee_p_list = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_zawody_list.txt'), 'r') as f:
        ns_zawody_list = eval(f.read())
    with open(os.path.join(args.newpath, 'ns_term_list.txt'), 'r') as f:
        ns_term_list = eval(f.read())
if not args.skip_old_overwrite:
    print('! Preparing old SIO data from source files...')
    (
        os_data_list,
        os_zawody_list,
        jsts_dict,
        jst_dict_rew,
        os_ee_sp_p_list,
        os_ee_sp_12_list,
        os_internaty_list) = get_os_data(oldpath)
    with open(os.path.join(args.newpath, 'os_data_list.txt'), 'w') as f:
        f.write(str(os_data_list))
    with open(os.path.join(args.newpath, 'os_zawody_list.txt'), 'w') as f:
        f.write(str(os_zawody_list))
    with open(os.path.join(args.newpath, 'jsts_dict.txt'), 'w') as f:
        f.write(str(jsts_dict))
    with open(os.path.join(args.newpath, 'jst_dict_rew.txt'), 'w') as f:
        f.write(str(jst_dict_rew))
    with open(os.path.join(args.newpath, 'os_ee_sp_p_list.txt'), 'w') as f:
        f.write(str(os_ee_sp_p_list))
    with open(os.path.join(args.newpath, 'os_ee_sp_12_list.txt'), 'w') as f:
        f.write(str(os_ee_sp_12_list))
    with open(os.path.join(args.newpath, 'os_internaty_list.txt'), 'w') as f:
        f.write(str(os_internaty_list))
else:
    print('* Loading prepared old SIO data from txt files...')
    with open(os.path.join(args.newpath, 'os_data_list.txt'), 'r') as f:
        os_data_list = eval(f.read())
    with open(os.path.join(args.newpath, 'os_zawody_list.txt'), 'r') as f:
        os_zawody_list = eval(f.read())
    with open(os.path.join(args.newpath, 'jsts_dict.txt'), 'r') as f:
        jsts_dict = eval(f.read())
    with open(os.path.join(args.newpath, 'jst_dict_rew.txt'), 'r') as f:
        jst_dict_rew = eval(f.read())
    with open(os.path.join(args.newpath, 'os_ee_sp_p_list.txt'), 'r') as f:
        os_ee_sp_p_list = eval(f.read())
    with open(os.path.join(args.newpath, 'os_ee_sp_12_list.txt'), 'r') as f:
        os_ee_sp_12_list = eval(f.read())
    with open(os.path.join(args.newpath, 'os_internaty_list.txt'), 'r') as f:
        os_internaty_list = eval(f.read())
for item in sio_report_list:
    print('* Generating %s...' % item[0])
    with open(os.path.join(item[2], item[1]), 'w') as f:
        cfile = csv.writer(f, delimiter=";", quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)
        if (
            item[1].startswith('os_') or
            item[1].startswith('etapy_') or
                item[1].startswith('osn_')):
            cfile.writerow([
                'ID organu scalającego',
                'Organ scalający',
                'Opis problemu',
                'Stare SIO',
                'Nowe SIO',
                'Nr RSPO',
                'REGON',
                'Typ jednostki',
                'Nazwa jednostki',
                'E-mail',
                'Telefon'])
        if (item[1] is 'etapy_eduk_szk_podst_ponizej_zero.csv'):
            for rn in ns_ee_sp_list:
                for ro in os_ee_sp_p_list:
                    if rn[0] == ro[0] and rn[10] == '.' and ro[1] != 0:
                        cfile.writerow([
                            ro[3],
                            jsts_dict[ro[3]],
                            'Niezgodność dotycząca etapu „Poniżej 0”',
                            'Wykazano wychowanków w etapie „Poniżej 0”',
                            'Etap „Poniżej 0” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif (item[1] is
                'etapy_eduk_przedszk_i_inne_formy_ponizej_zero.csv'):
            for rn in ns_ee_p_list:
                for ro in os_ee_sp_p_list:
                    if rn[0] == ro[0] and rn[10] == '.' and ro[1] != 0:
                        cfile.writerow([
                            ro[3],
                            jsts_dict[ro[3]],
                            'Niezgodność dotycząca etapu „Poniżej 0”',
                            'Wykazano wychowanków w etapie „Poniżej 0”',
                            'Etap „Poniżej 0” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif item[1] is 'etapy_eduk_szk_podst_zero.csv':
            for rn in ns_ee_sp_list:
                for ro in os_ee_sp_p_list:
                    if rn[0] == ro[0] and rn[11] == '.' and ro[2] != 0:
                        cfile.writerow([
                            ro[3],
                            jsts_dict[ro[3]],
                            'Niezgodność dotycząca etapu „0”',
                            'Wykazano wychowanków w etapie „0”',
                            'Etap „0” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif item[1] is 'etapy_eduk_przedszk_i_inne_formy_zero.csv':
            for rn in ns_ee_p_list:
                for ro in os_ee_sp_p_list:
                    if rn[0] == ro[0] and rn[11] == '.' and ro[2] != 0:
                        cfile.writerow([
                            ro[3],
                            jsts_dict[ro[3]],
                            'Niezgodność dotycząca etapu „0”',
                            'Wykazano wychowanków w etapie „0”',
                            'Etap „0” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif item[1] is 'etapy_eduk_szk_podst_pierwszy_etap.csv':
            for rn in ns_ee_sp_list:
                for ro in os_ee_sp_12_list:
                    l_1etap = ro[1] + ro[2] + ro[3]
                    if rn[0] == ro[0] and rn[12] == '.' and l_1etap != 0:
                        cfile.writerow([
                            ro[7],
                            jsts_dict[ro[7]],
                            'Niezgodność dotycząca I etapu eduk.',
                            'Wykazano uczniów w I etapie eduk.',
                            'Etap „I” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif item[1] is 'etapy_eduk_szk_podst_drugi_etap.csv':
            for rn in ns_ee_sp_list:
                for ro in os_ee_sp_12_list:
                    l_2etap = ro[4] + ro[5] + ro[6]
                    if rn[0] == ro[0] and rn[13] == '.' and l_2etap != 0:
                        cfile.writerow([
                            ro[7],
                            jsts_dict[ro[7]],
                            'Niezgodność dotycząca II etapu eduk.',
                            'Wykazano uczniów w II etapie eduk.',
                            'Etap „II” niewpisany w RSPO',
                            rn[0],
                            rn[1],
                            rn[4],
                            rn[3],
                            rn[5],
                            rn[6]])
        elif item[1] is 'os_all_items.csv':
            for row in os_data_list:
                cfile.writerow([
                    row[23],
                    jsts_dict[row[23]],
                    'brak problemu',
                    '',
                    '',
                    row[0],
                    row[1],
                    type_dict[row[4]],
                    row[7],
                    row[8],
                    row[9]])
        elif item[1] is 'os_brak_nr_rspo.csv':
            for row in os_data_list:
                if row[0] is 0 and row[4] not in (102, 103, 104, 109):
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Brak numeru RSPO w starym SIO',
                        'brak' if row[0] == 0 else row[0],
                        'nie badano',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'os_brak_adresu_email.csv':
            for row in os_data_list:
                if row[8] is '':
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Brak adresu e-mail w starym SIO',
                        'brak',
                        'nie badano',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'os_zdublowane_regony.csv':
            regon_list = [row[1] for row in os_data_list]
            dup_regon_list = duplicated_list(regon_list)
            for row in os_data_list:
                if row[1] in dup_regon_list:
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Zdublowany numer REGON w starym SIO',
                        row[1],
                        'nie badano',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'os_zdublowane_rspo.csv':
            rspo_list = [row[0] for row in os_data_list]
            dup_rspo_list = duplicated_list(rspo_list)
            for row in os_data_list:
                if row[0] in dup_regon_list:
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Zdublowany numer RSPO w starym SIO',
                        row[0],
                        'nie badano',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif (
            item[1] is
                'osn_nieznalezione_w_nowym_sio_zawody_wykazane_w_starym_sio\
                    .csv'):
            found = []
            ns_term_rspos = []
            for i in ns_term_list:
                ns_term_rspos.append(i[2])
            for ro in os_zawody_list:
                rofnd = False
                for rn in ns_zawody_list:
                    if str(ro[0]) + zawod_dict[ro[1]] == str(rn[0]) + rn[1]:
                        rofnd = True
                if rofnd is False:
                    found.append([ro[0], zawod_dict[ro[1]]])
            for rowo in os_data_list:
                for rowf in found:
                    if str(rowf[0]) in ns_term_rspos:
                        continue
                    if rowo[0] == rowf[0] and rowf[0] != 0:
                        for rown in ns_data_list:
                            if rowo[0] == rown[0]:
                                cfile.writerow([
                                    rowo[23],
                                    jsts_dict[rowo[23]],
                                    'Nieznaleziony w RSPO zawód',
                                    'istnieje',
                                    rowf[1],
                                    rowo[0],
                                    rowo[1],
                                    type_dict[rowo[4]],
                                    rowo[7],
                                    rowo[8],
                                    rowo[9]])
        elif item[1] is 'os_niepoprawne_numery_regon.csv':
            ns_long_regons = []
            for i in ns_data_list:
                if len(i[1]) == 9:
                    ns_long_regons.append(i[1] + '00000')
                else:
                    ns_long_regons.append(i[1])
            for r in ns_term_list:
                if len(r[0]) == 9:
                    ns_long_regons.append(r[0] + '00000')
                else:
                    ns_long_regons.append(r[0])
            for row in os_data_list:
                if row[1] not in ns_long_regons and row[0] is not 0:
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Nieznaleziony REGON ze starego SIO w nowym SIO',
                        row[1],
                        'nie badano',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'ns_brak_przypisanych_uczniow.csv':
            for rowo in os_data_list:
                for rown in ns_l_ucz_oddz:
                    if rowo[0] == rown[0] and rown[1] == 0:
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            ('Brak przypisanych uczniów w nowym SIO. '
                                'Komunikat w tej sprawie: '
                                'https://goo.gl/2WRcg5'),
                            'Nie badano',
                            rown[1],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'os_niepoprawne_numery_rspo.csv':
            for row in os_data_list:
                for i in ns_data_list:
                    if len(i[1]) == 9:
                        ns_long_regon = i[1] + '00000'
                    else:
                        ns_long_regon = i[1]
                    if row[1] == ns_long_regon and row[0] != i[0]:
                        cfile.writerow([
                            row[23],
                            jsts_dict[row[23]],
                            'Błędny nr RSPO w starym SIO',
                            row[0],
                            i[0],
                            row[0],
                            row[1],
                            type_dict[row[4]],
                            row[7],
                            row[8],
                            row[9]])
                for i in ns_term_list:
                    if len(i[1]) == 9:
                        ns_long_regon = i[1] + '00000'
                    else:
                        ns_long_regon = i[1]
                    if row[1] == ns_long_regon and row[0] != i[0]:
                        cfile.writerow([
                            row[23],
                            jsts_dict[row[23]],
                            'Błędny nr RSPO w starym SIO',
                            row[0],
                            i[0],
                            row[0],
                            row[1],
                            type_dict[row[4]],
                            row[7],
                            row[8],
                            row[9]])
        elif item[1] is 'osn_niezgodne_numery_regon.csv':
            for row in os_data_list:
                for i in ns_data_list:
                    if len(i[1]) == 9:
                        ns_long_regon = i[1] + '00000'
                    else:
                        ns_long_regon = i[1]
                    if row[1] != ns_long_regon and row[0] == i[0]:
                        cfile.writerow([
                            row[23],
                            jsts_dict[row[23]],
                            'Niezgodny nr REGON (wg nr RSPO)',
                            row[1],
                            ns_long_regon,
                            row[0],
                            row[1],
                            type_dict[row[4]],
                            row[7],
                            row[8],
                            row[9]])
                for i in ns_term_list:
                    if len(i[1]) == 9:
                        ns_long_regon = i[1] + '00000'
                    else:
                        ns_long_regon = i[1]
                    if row[1] != ns_long_regon and row[0] == i[0]:
                        cfile.writerow([
                            row[23],
                            jsts_dict[row[23]],
                            'Niezgodny nr REGON (wg nr RSPO)',
                            row[1],
                            ns_long_regon,
                            row[0],
                            row[1],
                            type_dict[row[4]],
                            row[7],
                            row[8],
                            row[9]])
        elif item[1] is 'osn_jst_problematyczne_numery_regon.csv':
            for row in os_data_list:
                if row[4] not in (103, 104, 109):
                    continue
                regon_found = False
                nregon = ''
                for i in ns_jst_list:
                    if row[1] == i[3] + '00000':
                        regon_found = True
                        continue
                if regon_found is False:
                    for i in ns_jst_list:
                        if i[2] == jsts_dict[row[23]]:
                            nregon = i[3]
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Niezgodny nr REGON JST lub CUW.',
                        row[1],
                        nregon,
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'osn_niepoprawne_pole_kategoria_uczniow.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0]:
                        kfound = False
                        for k in kat_ucz_dict[rowo[6]]:
                            if k in rown[9]:
                                kfound = True
                        if (
                            rown[4] == 'Szkoła policealna'
                            ' (ponadgimnazjalna)' and
                                kat_ucz_dict[rowo[6]][0] == 'Bez kategorii'):
                            kfound = True
                        if not kfound:
                            cfile.writerow([
                                rowo[23],
                                jsts_dict[rowo[23]],
                                'Niezgodność pola „Kategoria uczniów”',
                                kat_ucz_dict[rowo[6]][0],
                                rown[9],
                                rown[0],
                                rown[1],
                                rown[4],
                                rown[3],
                                rown[5],
                                rown[6]])
        elif item[1] is 'osn_niepoprawne_pole_typ.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and rowo[4] != rown[18]:
                        if (rowo[4] == 22 or rowo[4] == 23) and rown[18] == 85:
                            continue
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność pola „Typ jednostki”',
                            type_dict[rowo[4]],
                            rown[4],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_niepoprawne_pole_publicznosc.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and publ_dict[rowo[5]] != rown[8]:
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność pola „Publiczność”',
                            publ_dict[rowo[5]],
                            rown[8],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_nieskorygowana_nazwa_branzowki.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and (
                            'zasadnicza' in rowo[7].lower() or
                            'zasadnicza' in rown[3].lower()):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            ('Nieskorygowana nazwa „branżówki” w '
                                'starym lub nowym SIO'),
                            rowo[7],
                            rown[3],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_niezgodne_nazwy_jednostek.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    try:
                        onuni = unicode(rowo[7].decode(
                            'utf-8')).lower().strip()
                        nnuni = unicode(rown[3].decode(
                            'utf-8')).lower().strip()
                    except NameError:
                        onuni = rowo[7].lower().strip()
                        nnuni = rown[3].lower().strip()
                    if rowo[0] == rown[0] and onuni != nnuni:
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            ('Niezgodne nazwy w starym SIO i w RSPO. '
                                'Nazwy muszą być napisane zgodnie z zasadami '
                                'pisowni języka polskiego oraz '
                                'powinny być zgodne ze statutem. Przepisy '
                                'prawa o nazwach: https://goo.gl/nwe3vp '
                                'Narzędzie do sprawdzenia poprawności nazwy: '
                                'https://languagetool.org/pl/. '
                                'Polskie cudzysłowy: dolny „ (Alt + 0132) oraz'
                                ' górny ” (Alt + 0148). '
                                'Po skrócie „im.” musi być spacja! '
                                'Miejscowość, w której siedzibę ma publiczna '
                                'szkoła musi być częścią nazwy. '
                                'Patron szkoły publicznej jest '
                                'częścią nazwy szkoły. '
                                'Wielkość liter nie jest sprawdzana!'),
                            rowo[7],
                            rown[3],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    elif rowo[0] == rown[0] and 'niepubliczna' not in rown[
                        8] and (
                            (onuni.count(' ') < 3 and onuni.count(
                                ' w ') == 0) or
                            (nnuni.count(' ') < 3) and nnuni.count(
                                ' w ') == 0):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            ('Nazwa w starym SIO lub w RSPO niezgodna z '
                                'przepisami rozporządzenia: '
                                'https://goo.gl/nwe3vp'),
                            rowo[7],
                            rown[3],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    if rowo[0] == rown[0] and rowo[28] != '' and (
                            onuni.count(' im. ') == 0 or
                            nnuni.count(' im. ') == 0):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            ('Brak patrona: „%s” (wykazanego w starym SIO) '
                             'w nazwie '
                             'szkoły w starym SIO lub w RSPO. '
                             'Jeśli patrona nie ma, należy w starym SIO '
                             'pole „Patron” zostawić puste.' % (rowo[28])),
                            rowo[7],
                            rown[3],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_brakujace_zeasy_nowe_sio.csv':
            for rowo in os_data_list:
                if rowo[4] != 109:
                    continue
                zeas_found = False
                for rown in ns_jst_list:
                    ns_regon = rown[3] + '00000'
                    if (rowo[1] == ns_regon):
                        zeas_found = True
                        break
                if (zeas_found is False):
                    cfile.writerow([
                        rowo[23],
                        jsts_dict[rowo[23]],
                        'CUW nieznaleziony w nowym SIO',
                        'REGON CUW-u: ' + rowo[1],
                        'brak',
                        'jednostka pozarejestrowa',
                        rowo[1],
                        type_dict[rowo[4]],
                        rowo[7],
                        rowo[8],
                        rowo[9]])
        elif item[1] is 'osn_brakujace_zeasy_stare_sio.csv':
            for rown in ns_jst_list:
                if rown[0] != 160:
                    continue
                zeas_found = False
                for rowo in os_data_list:
                    ns_regon = rown[3] + '00000'
                    if (rowo[1] == ns_regon):
                        zeas_found = True
                        break
                if (zeas_found is False):
                    scalid = None
                    for r in os_data_list:
                        if rown[6] == jsts_dict[r[23]]:
                            scalid = r[23]
                            break
                    if scalid is not None:
                        cfile.writerow([
                            scalid,
                            rown[6],
                            'CUW nieznaleziony w starym SIO',
                            'brak',
                            'REGON CUW-u: ' + rown[3],
                            'jednostka pozarejestrowa',
                            rown[3],
                            rown[1],
                            rown[2],
                            rown[4],
                            rown[5]])
        elif item[1] is 'osn_rozne_jst_telefon.csv':
            for rowo in os_data_list:
                om = 'brak' if rowo[9] == '' else rowo[9]
                for rown in ns_jst_list:
                    if rown[0] != 103:  # do not check ZEAS 104 (temporary)
                        continue
                    ns_regon = rown[3] + '00000'
                    if (rowo[1] == ns_regon and
                            om.translate(None, '- ').lstrip('0') not in
                            rown[5].translate(None, '- ').lstrip('0')):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak numeru telefonu '
                            'JST',
                            'brak' if rowo[9] == '' else rowo[9],
                            'brak' if rown[5] == '' else rown[5],
                            'jednostka pozarejestrowa',
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_rozne_jst_email.csv':
            for rowo in os_data_list:
                om = 'brak' if rowo[8] == '' else rowo[8]
                for rown in ns_jst_list:
                    if rown[0] != 103:  # do not check ZEAS 104 (temporary)
                        continue
                    ns_regon = rown[3] + '00000'
                    if (rowo[1] == ns_regon and
                            om.lower() not in rown[4].lower()):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak e-mail JST',
                            'brak' if rowo[8] == '' else rowo[8],
                            'brak' if rown[4] == '' else rown[4],
                            'jednostka pozarejestrowa',
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    omed = 'brak' if rowo[19] == '' else rowo[19]
                    if (rowo[1] == ns_regon and
                            omed.lower() not in rown[4].lower() and
                            rown[0] == 103):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak e-mail komórki ds. edukacji '
                            '(adres ten w RSPO dodaje się jako *kolejny* adres'
                            ' e-mail w jednostce samorządu terytorialnego)',
                            'brak' if rowo[19] == '' else rowo[19],
                            'brak' if rown[4] == '' else rown[4],
                            'jednostka pozarejestrowa',
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_rozne_adresy_email.csv':
            for rowo in os_data_list:
                om = 'brak' if rowo[8] == '' else rowo[8]
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            om.lower() not in rown[5].lower()):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak adresu e-mail',
                            'brak' if rowo[8] == '' else rowo[8],
                            'brak' if rown[5] == '' else rown[5],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_rozne_nr_telefonu.csv':
            for rowo in os_data_list:
                om = 'brak' if rowo[9] == '' else rowo[9]
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            om.translate(None, '- ').lstrip('0') not in
                            rown[6].translate(None, '- ').lstrip('0')):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak numeru telefonu',
                            'brak' if rowo[9] == '' else rowo[9],
                            'brak' if rown[6] == '' else rown[6],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_brak_lub_niezgodny_org_nadrzedny.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            rowo[24] != rown[15] and
                            rowo[4] != 81 and
                            rowo[4] != 51 and
                            rowo[4] != 53 and
                            rowo[4] != 54 and
                            rowo[27] != 'filiaSzkolyPodst'):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność lub brak podmiotu nadrzędnego',
                            'Nr RSPO nadrzędnego: ' + (
                                'brak' if rowo[24] == 0 else str(rowo[24])),
                            'Nr RSPO nadrzędnego: ' + (
                                'brak' if rown[15] == 0 else str(rown[15])),
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_rozne_internaty.csv':
            for rowo in os_data_list:
                if rowo[0] == 0:
                    continue
                if rowo[0] in os_internaty_list:
                    for rown in ns_data_list:
                        if (
                            rowo[0] == rown[0] and
                                rown[14] == 0):
                            cfile.writerow([
                                rowo[23],
                                jsts_dict[rowo[23]],
                                'Niezgodność danych o internacie',
                                'Internat wpisany',
                                'Internat niewpisany w RSPO',
                                rowo[0],
                                rowo[1],
                                type_dict[rowo[4]],
                                rowo[7],
                                rowo[8],
                                rowo[9]])
                else:
                    for rown in ns_data_list:
                        if (
                            rowo[0] == rown[0] and
                                rown[14] == 1):
                            cfile.writerow([
                                rowo[23],
                                jsts_dict[rowo[23]],
                                'Niezgodność danych o internacie',
                                'Internat niewpisany',
                                'Internat wpisany w RSPO',
                                rowo[0],
                                rowo[1],
                                type_dict[rowo[4]],
                                rowo[7],
                                rowo[8],
                                rowo[9]])
        elif item[1] is 'osn_problematic_chars_in_names.csv':
            for rowo in os_data_list:
                if rowo[0] == 0:
                    continue
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            '\n' in rown[3].decode('utf-8')):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niedozwolone znaki w nazwie w RSPO',
                            'nie badano',
                            rown[3],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_niezgodny_typ_organu_prow.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (
                        rowo[0] == rown[0] and
                        typ_organu_prow_dict[rowo[21]] != rown[11] and
                            rown[13] == 'Nie dotyczy'):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność typu organu prowadzącego',
                            typ_organu_prow_dict[rowo[21]],
                            rown[11],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    elif (
                        rowo[0] == rown[0] and
                        rown[13] == 'Część gminna' and
                        (typ_organu_prow_dict[rowo[21]] != rown[11] and
                         typ_organu_prow_dict[rowo[21]] != 'Gmina')):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność typu organu prowadzącego',
                            typ_organu_prow_dict[rowo[21]],
                            rown[11],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    elif (
                        rowo[0] == rown[0] and
                        rown[13] == 'Część powiatowa' and
                            typ_organu_prow_dict[rowo[21]] != rown[11]):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność typu organu prowadzącego',
                            typ_organu_prow_dict[rowo[21]],
                            rown[11],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    elif (
                        rowo[0] == rown[0] and
                            rown[12] == 'DANE DO UZUPEŁNIENIA'):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niepoprawny organ prowadzący w RSPO',
                            typ_organu_prow_dict[rowo[21]],
                            rown[12],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_niepoprawne_pole_specyfika.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            specyfika_dict[rowo[20]] != rown[10]):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność pola „Specyfika”',
                            specyfika_dict[rowo[20]],
                            rown[10],
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif item[1] is 'osn_niezgodne_dane_o_obwodowosci.csv':
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and rown[17] == 0 and
                            rowo[22] == 'true'):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność danych o obwodowości',
                            'Szkoła obwodowa',
                            'Obwód niewpisany',
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
                    elif (rowo[0] == rown[0] and rown[17] == 1 and
                            rowo[22] == 'false'):
                        cfile.writerow([
                            rowo[23],
                            jsts_dict[rowo[23]],
                            'Niezgodność danych o obwodowości',
                            'Szkoła nieobwodowa',
                            'Obwód wpisany',
                            rowo[0],
                            rowo[1],
                            type_dict[rowo[4]],
                            rowo[7],
                            rowo[8],
                            rowo[9]])
        elif (item[1] is
                'osn_brakujace_w_starym_sio_numery_regon_z_nowego_sio.csv'):
            os_regons = []
            for i in os_data_list:
                os_regons.append(i[1])
            for row in ns_data_list:
                if row[1] in missregons:
                    print('! EXCEPTION! REGON skipped: ' + row[1])
                    continue
                if len(row[1]) == 9:
                    reg_long = row[1] + '00000'
                else:
                    reg_long = row[1]
                try:
                    roz_date = datetime.strptime(row[7], '%Y-%m-%d')
                except BaseException:
                    roz_date = datetime.strptime('9999-01-01', '%Y-%m-%d')
                if (reg_long not in os_regons and
                        'MINISTERSTWO' not in row[2] and
                        roz_date < BORDER_DATE):
                    try:
                        cfile.writerow([
                            jst_dict_rew[row[2]],
                            row[2],
                            'Jednostka brakująca w starym SIO '
                            '(wg nr REGON)',
                            'brak jednostki',
                            'jednostka istnieje',
                            row[0],
                            row[1],
                            row[4],
                            row[3],
                            row[5],
                            row[6]])
                    except KeyError:
                        cfile.writerow([
                            'niescalona jst',
                            row[2],
                            'Jednostka brakująca w starym SIO '
                            '(wg nr REGON)',
                            'brak jednostki',
                            'jednostka istnieje',
                            row[0],
                            row[1],
                            row[4],
                            row[3],
                            row[5],
                            row[6]])
        elif (item[1] is
                'osn_nieistniejace_szkoly_wykazane_w_starym_sio.csv'):
            ns_regons = []
            for row in ns_data_list:
                if len(row[1]) == 9:
                    ns_regons.append(row[1] + '00000')
                else:
                    ns_regons.append(row[1])
            for i in ns_term_list:
                if datetime.strptime(i[1], '%Y-%m-%d') >= BORDER_DATEZ:
                    if len(i[0]) == 9:
                        ns_regons.append(i[0] + '00000')
                    else:
                        ns_regons.append(i[0])
            for row in os_data_list:
                if row[1] not in ns_regons and row[4] < 101:
                    cfile.writerow([
                        row[23],
                        jsts_dict[row[23]],
                        'Nieistniejąca jednostka wykazana w '
                        'starym SIO (wg nr REGON)',
                        'jednostka istnieje',
                        'brak jednostki',
                        row[0],
                        row[1],
                        type_dict[row[4]],
                        row[7],
                        row[8],
                        row[9]])
        elif item[1] is 'ns_all_items.csv':
            for row in ns_data_list:
                cfile.writerow(row)

generate_jst_reports()

# convert CSV into XLSX
if os.path.exists(os.path.join('!critical!', 'XLSX')):
    shutil.rmtree(os.path.join('!critical!', 'XLSX'))
    os.makedirs(os.path.join('!critical!', 'XLSX'))
else:
    os.makedirs(os.path.join('!critical!', 'XLSX'))

for i in sio_report_list:
    print('* XLSX: Generating %s.xlsx' % os.path.splitext(i[1])[0])
    workbook = Workbook(os.path.join('!critical!', 'XLSX',
                        os.path.splitext(i[1])[0] + '.xlsx'))
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    with open(os.path.join(i[2], i[1]), 'r') as f:
        reader = csv.reader(f, delimiter=';', quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                if r == 0:
                    try:
                        worksheet.write(r, c, col.decode('utf-8'), bold)
                    except AttributeError:
                        worksheet.write(r, c, col, bold)
                else:
                    try:
                        worksheet.write(r, c, col.decode('utf-8'))
                    except AttributeError:
                        worksheet.write(r, c, col)
        worksheet.autofilter(0, 0, r, c)
        worksheet.set_column(0, c, 30)
    workbook.close()

# move CSV files to CSV directory
if os.path.exists(os.path.join('!critical!', 'CSV')):
    shutil.rmtree(os.path.join('!critical!', 'CSV'))
    os.makedirs(os.path.join('!critical!', 'CSV'))
else:
    os.makedirs(os.path.join('!critical!', 'CSV'))
for filename in glob.glob(os.path.join('!critical!', '*.csv')):
    shutil.move(filename, os.path.join('!critical!', 'CSV'))

print('* Execution time: ' + str(time.clock() - start))
