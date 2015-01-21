#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

# TODO optionally more extensive e-mail checking

from __future__ import print_function
from lxml import etree
from collections import Counter
from datetime import datetime
from validate_email import validate_email
from dictionaries import kat_ucz_dict
from dictionaries import publ_dict
from dictionaries import type_dict
from dictionaries import specyfika_dict
from dictionaries import zawod_dict
from dictionaries import typ_organu_prow_dict
import argparse
import os
import csv
import difflib
import shutil
import sys

XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}
XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
         'x': 'urn:schemas-microsoft-com:office:excel',
         'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

BORDER_DATE = datetime.strptime('2014-09-30', '%Y-%m-%d')
BORDER_DATEZ = datetime.strptime('2013-08-31', '%Y-%m-%d')

parser = argparse.ArgumentParser()
parser.add_argument("oldpath", help="path to DIR with old SIO XML files")
parser.add_argument('newpath', help='path to DIR with new SIO XLS files')
parser.add_argument('-t', "--ns-mail-tough-check",
                    help="NSIO: e-mails tough checking",
                    action="store_true")
parser.add_argument("--stages",
                    help="NSIO: education stages reports",
                    action="store_true")
parser.add_argument("--move",
                    help="move reports to 'src' directory",
                    action="store_true")
parser.add_argument("--compare",
                    help="compare new reports with old reports",
                    action="store_true")
args = parser.parse_args()


def compare_csvs(sio_report_list):
    for item in sio_report_list:
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
            continue
        print('******')

sio_report_list = ([
    ['OS: all items', 'os_all_items.csv', '!normal!'],
    ['OS: duplicated REGONs', 'os_zdublowane_regony.csv', '!critical!'],
    ['OS: duplicated RSPOs', 'os_zdublowane_nr_rspo.csv', '!critical!'],
    ['OS: no RSPOs', 'os_brak_nr_rspo.csv', '!critical!'],
    ['OS: no e-mails', 'os_brak_adresu_email.csv', '!critical!'],
    ['OS: incorrect e-mails', 'os_nieprawidlowe_adresy_email.csv', '!normal!'],
    ['OS: incorrect RSPOs', 'os_niepoprawne_numery_rspo.csv', '!critical!'],
    ['OS: incorrect REGONSs', 'os_niepoprawne_numery_regon.csv', '!critical!'],
    ['OS: incorrect publicznosc', 'osn_niepoprawne_pole_publicznosc.csv',
        '!critical!'],
    ['OS: incorrect kategoria uczniow',
        'osn_niepoprawne_pole_kategoria_uczniow.csv', '!critical!'],
    ['NS: all items', 'ns_all_items.csv', '!normal!'],
    ['NS: no e-mails', 'ns_brak_adresu_email.csv', '!normal!'],
    ['NS: Missing REGONs in old SIO existing in a new SIO with birthdate '
        'earlier than %s' % BORDER_DATE,
     'ns_brakujace_w_starym_sio_numery_regon_z_nowego_sio.csv', '!critical!'],
    ['NS: Missing REGONs in new SIO existing in a old SIO',
     'ns_brakujace_w_nowym_sio_numery_regon_ze_starego_sio.csv', '!critical!'],
    ['OS: incorrect type', 'osn_niepoprawne_pole_typ.csv', '!critical!'],
    ['OS: incorrect specyfika', 'osn_niepoprawne_pole_specyfika.csv',
        '!critical!'],
    ['OS: incorrect typ organu', 'osn_niezgodny_typ_organu_prow.csv',
        '!critical!'],
    ['OS: different jobs',
        'osn_nieznalezione_w_nowym_sio_zawody_wykazane_w_starym_sio.csv',
        '!critical!'],
    ['NS: different jobs',
        'osn_nieznalezione_w_starym_sio_zawody_wykazane_w_nowym_sio.csv',
        '!critical!'],
    ['NS: incorrect szkolaObwodowa',
        'osn_niezgodne_dane_o_obowodowosci.csv',
        '!critical!'],
    ['NS: incorrect e-mails', 'ns_nieprawidlowe_adresy_email.csv', '!normal!'],
    ['NS: different e-mails', 'osn_rozne_adresy_email.csv', '!normal!']
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
    'czy obwodowa?'
]


def get_ns_obwody(path):
    tree = etree.parse(os.path.join(path, 'obwody.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    for i in tree.xpath('//ss:Cell[@ss:Index="1"]/ss:Data/text()',
                        namespaces=XLSNS):
        try:
            data.append(xi(i))
        except:
            continue
    return set(data)


def get_ns_zawody(path):
    tree = etree.parse(os.path.join(path, 'zawody.xls'))
    print('* %s' % tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    data = []
    ns_rspos = []
    ns_zawody = []
    for i in tree.xpath('//ss:Cell[@ss:Index="1"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_rspos.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="4"]/ss:Data/text()',
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
        except:
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
    return unicode(s).encode('utf8')


def xi(s):
    if s is None:
        return 0
    return int(s)


def os_row(i, a):
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
        xs(i.get('szkolaObwodowa'))
    ]
    return lista


def get_os_ee_data(path, etap, typ_szk):
    if etap == 'pon_zero':
        u3 = 'u3_3_1'
    elif etap == 'zero':
        u3 = 'u3_3_2'

    def get_os_ee_row(tree, u3):
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
                except:
                    nrRspo = 0
                try:
                    l_ucz = tree.xpath(
                        '//' + typ + '/uczniowieSzkolyPodst/'
                        'oddzialyPrzedszkolne[@numerIdent="' +
                        i.get('numerIdent')[:-1] + '1' +
                        '"]/dzieciWgOddzialow/u3_3/' + u3,
                        namespaces=XSNS)[0].get('kol2')
                except:
                    l_ucz = '0'
                file_rows.append([nrRspo, l_ucz])
        return file_rows
    data = []
    for root, dirs, files in os.walk(path):
        for single_file in files:
            if single_file.endswith('.xml'):
                single_file_path = os.path.join(root, single_file)
                single_file_tree = etree.parse(single_file_path)
                data = data + get_os_ee_row(single_file_tree, u3)
    return(data)


def get_os_row(tree):
    file_rows = []
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        file_rows.append(os_row(i, a))
    return file_rows


def get_os_data(path):
    data = []
    os_zawody = []
    for root, dirs, files in os.walk(path):
        for single_file in files:
            if single_file.endswith('.xml'):
                single_file_path = os.path.join(root, single_file)
                single_file_tree = etree.parse(single_file_path)
                data = data + get_os_row(single_file_tree)
                if get_os_zawody(single_file_tree) != []:
                    for r in get_os_zawody(single_file_tree):
                        os_zawody.append(r)
    return(data, os_zawody)


def get_terminated_id(tree, id):
    lista = []
    print('* ' + tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                            namespaces=XLSNS)[0])
    lista = lista + tree.xpath(
        '//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
        namespaces=XLSNS
    )[1:]
    return lista


def get_ns_ee_data(path, typ):
    tree = etree.parse(os.path.join(path, 'ee_' + typ + '.xls'))
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
    # for 'ponizej zero' col skipped first merged cell
    for i in tree.xpath('//ss:Cell[@ss:Index="4"]/ss:Data/text()',
                        namespaces=XLSNS)[1:]:
        ns_ee_pzero.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="5"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_ee_zero.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="6"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_ee_first.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="7"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_ee_second.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="8"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_ee_irrelevant.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="1"]/ss:Data/text()',
                        namespaces=XLSNS):
        try:
            ns_rspos.append(xi(i))
        except:
            ns_rspos.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="13"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_regons.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="2"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_typs.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="3"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_names.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="10"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_org_rej.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="36"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_datas_rozp_dzial.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="33"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_publicznosc.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="32"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_kat_uczn.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="26"]/ss:Data',
                        namespaces=XLSNS):
        if i.text is None:
            ns_emails.append('')
        else:
            ns_emails.append(i.text)
    for i in tree.xpath('//ss:Cell[@ss:Index="24"]/ss:Data',
                        namespaces=XLSNS):
        if i.text is None:
            ns_tels.append('')
        else:
            ns_tels.append(i.text)
    dataee = zip(ns_rspos, ns_regons, ns_org_rej, ns_names, ns_typs, ns_emails,
                 ns_tels, ns_datas_rozp_dzial, ns_publicznosc, ns_kat_uczn,
                 ns_ee_pzero, ns_ee_zero, ns_ee_first, ns_ee_second,
                 ns_ee_irrelevant)
    return dataee


def get_ns_data(path):
    tree = etree.parse(os.path.join(path, 'rspo_aktywne.xls'))
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
    for i in tree.xpath('//ss:Cell[@ss:Index="1"]/ss:Data/text()',
                        namespaces=XLSNS):
        try:
            ns_rspos.append(xi(i))
        except:
            ns_rspos.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="9"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_regons.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="2"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_typs.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="3"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_names.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="6"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_org_rej.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="34"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_datas_rozp_dzial.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="28"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_publicznosc.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="27"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_kat_uczn.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="21"]/ss:Data',
                        namespaces=XLSNS):
        if i.text is None:
            ns_emails.append('')
        else:
            ns_emails.append(i.text)
    # for Telefon col skipped first merged cell
    for i in tree.xpath('//ss:Cell[@ss:Index="19"]/ss:Data',
                        namespaces=XLSNS)[1:]:
        if i.text is None:
            ns_tels.append('')
        else:
            ns_tels.append(i.text)
    for i in tree.xpath('//ss:Cell[@ss:Index="26"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_specyfika.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="7"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_typ_org_prow.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="8"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_org_prow.append(xs(i))
    for i in tree.xpath('//ss:Cell[@ss:Index="23"]/ss:Data/text()',
                        namespaces=XLSNS):
        ns_czesc_miejska.append(xs(i))

    data = zip(ns_rspos, ns_regons, ns_org_rej, ns_names, ns_typs, ns_emails,
               ns_tels, ns_datas_rozp_dzial, ns_publicznosc, ns_kat_uczn,
               ns_specyfika, ns_typ_org_prow, ns_org_prow, ns_czesc_miejska)
    return data

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
ns_zawody_list = get_ns_zawody(args.newpath)
print('* Loading new SIO data...')
ns_data_list = get_ns_data(args.newpath)
term_tree = etree.parse(os.path.join(args.newpath, 'rspo_nieaktywne.xls'))
ns_term_list = zip(
    get_terminated_id(term_tree, '10'),  # REGON
    get_terminated_id(term_tree, '5'),   # Termination date
    get_terminated_id(term_tree, '1')    # Nr RSPO
)
print('* Loading old SIO data...')
os_data_list, os_zawody_list = get_os_data(args.oldpath)
if args.stages:
    if not os.path.exists(os.path.join('!ee!')):
        os.makedirs(os.path.join('!ee!'))
    ee_report_list = ([
        ['EE SP: ponizej zero', 'ee_sp_ponizej_zero.csv', '!ee!'],
        ['EE SP: zero', 'ee_sp_zero.csv', '!ee!'],
        ['EE P: ponizej zero', 'ee_p_ponizej_zero.csv', '!ee!'],
        ['EE P: zero', 'ee_p_zero.csv', '!ee!'],
        ['EE SP: pierwszy etap', 'ee_sp_pierwszy_etap.csv', '!ee!'],
        ['EE SP: drugi etap', 'ee_sp_drugi_etap.csv', '!ee!']
    ])
    print('* Loading education stages old SIO data...')
    os_ee_sp_zero_list = get_os_ee_data(args.oldpath, 'zero', 'sp')
    os_ee_sp_ponzero_list = get_os_ee_data(args.oldpath, 'pon_zero', 'sp')
    os_ee_p_zero_list = get_os_ee_data(args.oldpath, 'zero', 'p')
    os_ee_p_ponzero_list = get_os_ee_data(args.oldpath, 'pon_zero', 'p')
    print('* Loading education stages new SIO data...')
    ns_ees_data_list = get_ns_ee_data(os.path.join(args.newpath), 'sp')
    ns_eep_data_list = get_ns_ee_data(os.path.join(args.newpath), 'przedszk')
    for item in ee_report_list:
        print('* Generating %s...' % item[0])
        with open(os.path.join(item[2], item[1]), 'wb') as f:
            cfile = csv.writer(f, delimiter=";", quotechar='"',
                               quoting=csv.QUOTE_NONNUMERIC)
            if item[1] is 'ee_sp_ponizej_zero.csv':
                for rn in ns_ees_data_list:
                    for ro in os_ee_sp_ponzero_list:
                        if rn[0] == ro[0] and rn[10] == '.' and ro[1] != '0':
                            cfile.writerow(rn)
            elif item[1] is 'ee_p_ponizej_zero.csv':
                for rn in ns_eep_data_list:
                    for ro in os_ee_p_ponzero_list:
                        if(rn[0] == ro[0]):
                            print(rn[0], ro[0], rn[10], ro[1])
                        if rn[0] == ro[0] and rn[10] == '.' and ro[1] != '0':
                            cfile.writerow(rn)
    sys.exit()
if not os.path.exists(os.path.join('!normal!')):
    os.makedirs(os.path.join('!normal!'))
if not os.path.exists(os.path.join('!critical!')):
    os.makedirs(os.path.join('!critical!'))
for item in sio_report_list:
    print('* Generating %s...' % item[0])
    with open(os.path.join(item[2], item[1]), 'wb') as f:
        cfile = csv.writer(f, delimiter=";", quotechar='"',
                           quoting=csv.QUOTE_NONNUMERIC)
        if item[1].startswith('os_'):
            cfile.writerow(header_list)
        if item[1] is 'os_all_items.csv':
            for row in os_data_list:
                cfile.writerow(row)
        elif item[1] is 'os_brak_nr_rspo.csv':
            for row in os_data_list:
                if row[0] is 0 and row[4] not in (102, 103, 104):
                    cfile.writerow(row)
        elif item[1] is 'os_brak_adresu_email.csv':
            for row in os_data_list:
                if row[8] is '':
                    cfile.writerow(row)
        elif item[1] is 'os_zdublowane_regony.csv':
            regon_list = [row[1] for row in os_data_list]
            dup_regon_list = duplicated_list(regon_list)
            for row in os_data_list:
                if row[1] in dup_regon_list:
                    cfile.writerow(row)
        elif item[1] is 'os_zdublowane_nr_rspo.csv':
            rspo_list = [row[0] for row in os_data_list]
            dup_rspo_list = duplicated_list(rspo_list)
            for row in os_data_list:
                if row[0] in dup_rspo_list and row[0] is not 0:
                    cfile.writerow(row)
        elif item[1] is 'os_nieprawidlowe_adresy_email.csv':
            for row in os_data_list:
                if (not validate_email(row[8])
                        and row[8] is not '') or '@02.pl' in row[8]:
                    cfile.writerow(row)
        elif (
            item[1] is
            'osn_nieznalezione_w_nowym_sio_zawody_wykazane_w_starym_sio.csv'
        ):
            found = []
            ns_term_rspos = []
            for i in ns_term_list:
                ns_term_rspos.append(i[2])
            for ro in os_zawody_list:
                rofnd = False
                for rn in ns_zawody_list:
                    if str(ro[0]) + zawod_dict[ro[1]] == str(rn[0]) + rn[1]:
                        rofnd = True
                if rofnd == False:
                    found.append([ro[0], zawod_dict[ro[1]]])
            cfile.writerow(['Nieznalezione w nowym SIO zawody',
                            ] + header_list[:-7])
            for rowo in os_data_list:
                for rowf in found:
                    if str(rowf[0]) in ns_term_rspos:
                        continue
                    if rowo[0] == rowf[0] and rowf[0] != 0:
                        cfile.writerow([rowf[1]] + rowo[:-7])
        elif (
            item[1] is
            'osn_nieznalezione_w_starym_sio_zawody_wykazane_w_nowym_sio.csv'
        ):
            foundn = []
            for rn in ns_zawody_list:
                rofod = False
                for ro in os_zawody_list:
                    if str(ro[0]) + zawod_dict[ro[1]] == str(rn[0]) + rn[1]:
                        rofod = True
                if rofod == False:
                    foundn.append([rn[0], rn[1]])
            cfile.writerow(
                ['Nieznalezione w starym SIO zawody'] + list(ns_data_list[0])
            )
            for rown in ns_data_list[1:]:
                for rowf in foundn[1:]:
                    if (
                        rown[0] == int(rowf[0]) and
                        int(rowf[0]) != 0 and
                        'MINISTERSTWO' not in rown[2]
                    ):
                        cfile.writerow([rowf[1]] + list(rown))
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
                    cfile.writerow(row)
        elif item[1] is 'os_niepoprawne_numery_rspo.csv':
            ns_rspos = []
            for i in ns_data_list:
                ns_rspos.append(i[0])
            for i in ns_term_list:
                ns_rspos.append(int(i[2]))
            for row in os_data_list:
                if row[0] not in ns_rspos and row[0] is not 0:
                    cfile.writerow(row)
        elif item[1] is 'osn_niepoprawne_pole_kategoria_uczniow.csv':
            cfile.writerow(['Stare SIO (prawdopodobnie błędnie)',
                            'Nowe SIO (prawdopodobnie poprawnie)',
                            'Organ rejestrujący'] + header_list[:-7])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0]:
                        kfound = False
                        for k in kat_ucz_dict[rowo[6]]:
                            if k in rown[9]:
                                kfound = True
                        if not kfound:
                            cfile.writerow([kat_ucz_dict[rowo[6]][0],
                                            rown[9], rown[2]] + rowo[:-7])
        elif item[1] is 'osn_niepoprawne_pole_typ.csv':
            cfile.writerow(['Stare SIO (prawdopodobnie błędnie)',
                            'Nowe SIO (prawdopodobnie poprawnie)',
                            'Organ rejestrujący'] + header_list[:-7])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and type_dict[rowo[4]] != rown[4]:
                        cfile.writerow([type_dict[rowo[4]], rown[4],
                                        rown[2]] + rowo[:-7])
        elif item[1] is 'osn_niepoprawne_pole_publicznosc.csv':
            cfile.writerow(['Stare SIO (na 95 proc. błędnie)',
                            'Nowe SIO (na 95 proc. poprawnie)',
                            'Organ rejestrujący'] + header_list[:-7])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and publ_dict[rowo[5]] != rown[8]:
                        cfile.writerow([publ_dict[rowo[5]], rown[8],
                                        rown[2]] + rowo[:-7])
        elif item[1] is 'ns_all_items.csv':
            for row in ns_data_list:
                cfile.writerow(row)
        elif item[1] is 'ns_brak_adresu_email.csv':
            for row in ns_data_list:
                if ((row[5] is '' or 'E-mail' in row[5])
                        and ('MINISTERSTWO' not in row[2])):
                    cfile.writerow(row)
        elif item[1] is 'osn_rozne_adresy_email.csv':
            cfile.writerow(['Stare SIO (prawdopodobnie błędnie)',
                            'Nowe SIO (prawdopodobnie poprawnie)',
                            'Organ rejestrujący'] + header_list)
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            rowo[8].lower() not in rown[5].lower()):
                        cfile.writerow([rowo[8], rown[5], rown[2]] + rowo)
        elif item[1] is 'osn_niezgodny_typ_organu_prow.csv':
            cfile.writerow(['Stare SIO - typ organu prow.',
                            'Stare SIO - nazwa organu prow.',
                            'Nowe SIO - typ organu prow.',
                            'Nowe SIO - nazwa organu prow.',
                            'Nowe SIO - część miejska',
                            'Organ rejestrujący'] + header_list[:-7])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (
                        rowo[0] == rown[0] and
                        typ_organu_prow_dict[rowo[21]] != rown[11] and
                        rown[13] == 'Nie dotyczy'
                    ):
                        cfile.writerow([typ_organu_prow_dict[rowo[21]],
                                        rowo[15],
                                        rown[11],
                                        rown[12],
                                        rown[13],
                                        rown[2]] + rowo[:-7])
                    elif (
                        rowo[0] == rown[0] and
                        rown[13] == 'Część gminna' and
                        (typ_organu_prow_dict[rowo[21]] != rown[11] and
                         typ_organu_prow_dict[rowo[21]] != 'Gmina')
                    ):
                        cfile.writerow([typ_organu_prow_dict[rowo[21]],
                                        rowo[15],
                                        rown[11],
                                        rown[12],
                                        rown[13],
                                        rown[2]] + rowo[:-7])
                    elif (
                        rowo[0] == rown[0] and
                        rown[13] == 'Część powiatowa' and
                        typ_organu_prow_dict[rowo[21]] != rown[11]
                    ):
                        cfile.writerow([typ_organu_prow_dict[rowo[21]],
                                        rowo[15],
                                        rown[11],
                                        rown[12],
                                        rown[13],
                                        rown[2]] + rowo[:-7])
        elif item[1] is 'osn_niepoprawne_pole_specyfika.csv':
            cfile.writerow(['Stare SIO (prawdopodobnie błędnie)',
                            'Nowe SIO (prawdopodobnie poprawnie)',
                            'Organ rejestrujący'] + header_list[:-7])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if (rowo[0] == rown[0] and
                            specyfika_dict[rowo[20]] != rown[10]):
                        cfile.writerow([specyfika_dict[rowo[20]], rown[10],
                                        rown[2]] + rowo[:-7])
        elif item[1] is 'osn_niezgodne_dane_o_obowodowosci.csv':
            cfile.writerow(['Stare SIO',
                            'Nowe SIO'] + header_list[:-7])
            obw_rspo_list = get_ns_obwody(args.newpath)
            for rowo in os_data_list:
                    if (rowo[0] not in obw_rspo_list and rowo[22] == 'true'):
                        cfile.writerow(
                            ['Szkoła obwodowa', 'Obwód niewpisany'] + rowo[:-7]
                        )
                    elif (rowo[0] in obw_rspo_list and rowo[22] == 'false'):
                        cfile.writerow(
                            ['Szkoła nieobwodowa', 'Obwód wpisany'] + rowo[:-7]
                        )
        elif (item[1] is
                'ns_brakujace_w_starym_sio_numery_regon_z_nowego_sio.csv'):
            os_regons = []
            for i in os_data_list:
                os_regons.append(i[1])
            for row in ns_data_list:
                if len(row[1]) == 9:
                    reg_long = row[1] + '00000'
                else:
                    reg_long = row[1]
                try:
                    roz_date = datetime.strptime(row[7], '%Y-%m-%d')
                except:
                    roz_date = datetime.strptime('9999-01-01', '%Y-%m-%d')
                if (reg_long not in os_regons and 'MINISTERSTWO' not in row[2]
                        and roz_date < BORDER_DATE) or row[0] == 'Nr RSPO':
                    cfile.writerow(row)
        elif (item[1] is
                'ns_brakujace_w_nowym_sio_numery_regon_ze_starego_sio.csv'):
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
                    cfile.writerow(row)
        elif item[1] is 'ns_nieprawidlowe_adresy_email.csv':
            for row in ns_data_list:
                ms = row[5].split(' , ')
                for m in ms:
                    if args.ns_mail_tough_check:
                        print('* Checking: ' + m)
                        if (not validate_email(m, check_mx=True)
                                and m is not '') or '@02.pl' in m:
                            cfile.writerow(row)
                    else:
                        if (not validate_email(m)
                                and m is not '') or '@02.pl' in m:
                            cfile.writerow(row)
