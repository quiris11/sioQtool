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
import argparse
import os
import csv
# import sys

XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}
XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
         'x': 'urn:schemas-microsoft-com:office:excel',
         'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

BORDER_DATE = datetime.strptime('2014-09-30', '%Y-%m-%d')

parser = argparse.ArgumentParser()
parser.add_argument("oldpath", help="path to DIR with old SIO XML files")
parser.add_argument('newpath', help='path to DIR with new SIO XLS files')
parser.add_argument('-t', "--ns-mail-tough-check",
                    help="NSIO: e-mails tough checking",
                    action="store_true")
args = parser.parse_args()

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
        'osn_niepoprawne_pole_kategoria_uczniow.csv', '!normal!'],
    ['NS: all items', 'ns_all_items.csv', '!normal!'],
    ['NS: no e-mails', 'ns_brak_adresu_email.csv', '!normal!'],
    ['NS: Missing REGONs existing in a new SIO with birthdate earlier '
        'than %s' % BORDER_DATE,
     'ns_brakujace_w_starym_sio_numery_regon_z_nowego_sio.csv', '!critical!'],
    ['NS: incorrect e-mails', 'ns_nieprawidlowe_adresy_email.csv', '!normal!']
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
    'email kom.'
]


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
        xs(a.get('emailKomorki'))
    ]
    return lista


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
    for root, dirs, files in os.walk(path):
        for single_file in files:
            if single_file.endswith('.xml'):
                single_file_path = os.path.join(root, single_file)
                single_file_tree = etree.parse(single_file_path)
                data = data + get_os_row(single_file_tree)
    return(data)


def get_terminated_id(path, id):
    lista = []
    for i in ('000038z.xls', '000038b.xls'):
        tree = etree.parse(os.path.join(path, i))
        print('* ' + tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                                namespaces=XLSNS)[0])
        lista = lista + tree.xpath(
            '//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
            namespaces=XLSNS
        )[1:]
    return lista


def get_ns_data(path):
    tree = etree.parse(os.path.join(path, '000038.xls'))
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
    data = zip(ns_rspos, ns_regons, ns_org_rej, ns_names, ns_typs, ns_emails,
               ns_tels, ns_datas_rozp_dzial, ns_publicznosc, ns_kat_uczn)
    return data

print('* Loading new SIO data...')
ns_data_list = get_ns_data(args.newpath)
print('* Loading old SIO data...')
os_data_list = get_os_data(args.oldpath)
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
        elif item[1] is 'os_niepoprawne_numery_regon.csv':
            ns_long_regons = []
            for i in ns_data_list:
                if len(i[1]) == 9:
                    ns_long_regons.append(i[1] + '00000')
                else:
                    ns_long_regons.append(i[1])
            for i in get_terminated_id(args.newpath, '10'):
                if len(i) == 9:
                    ns_long_regons.append(i + '00000')
                else:
                    ns_long_regons.append(i)
            for row in os_data_list:
                if row[1] not in ns_long_regons and row[0] is not 0:
                    cfile.writerow(row)
        elif item[1] is 'os_niepoprawne_numery_rspo.csv':
            ns_rspos = []
            for i in ns_data_list:
                ns_rspos.append(i[0])
            for i in get_terminated_id(args.newpath, '1'):
                ns_rspos.append(int(i))
            for row in os_data_list:
                if row[0] not in ns_rspos and row[0] is not 0:
                    cfile.writerow(row)
        elif item[1] is 'osn_niepoprawne_pole_kategoria_uczniow.csv':
            kat_ucz_dict = {
                1: 'Dzieci lub młodzież',
                2: 'Dorośli',
                3: 'Bez kategorii',
            }
            ns_rspos = []
            cfile.writerow(header_list + ['Stare SIO (prawdopodobnie błędnie)',
                           'Nowe SIO (prawdopodobnie poprawnie)'])
            for i in ns_data_list:
                ns_rspos.append(i[0])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and kat_ucz_dict[rowo[6]] != rown[9]:
                        cfile.writerow(rowo + [kat_ucz_dict[rowo[6]], rown[9]])
        elif item[1] is 'osn_niepoprawne_pole_publicznosc.csv':
            publ_dict = {
                1: 'publiczna',
                2: 'niepubliczna o uprawnieniach szkoły publicznej',
                3: 'niepubliczna bez uprawnień szkoły publicznej',
                4: 'niepubliczna'
            }
            ns_rspos = []
            cfile.writerow(['Stare SIO (na 95 proc. błędnie)',
                            'Nowe SIO (na 95 proc. poprawnie)',
                            'Organ rejestrujący'] + header_list)
            for i in ns_data_list:
                ns_rspos.append(i[0])
            for rowo in os_data_list:
                for rown in ns_data_list:
                    if rowo[0] == rown[0] and publ_dict[rowo[5]] != rown[8]:
                        cfile.writerow([publ_dict[rowo[5]], rown[8],
                                        rown[2]] + rowo)
        elif item[1] is 'ns_all_items.csv':
            for row in ns_data_list:
                cfile.writerow(row)
        elif item[1] is 'ns_brak_adresu_email.csv':
            for row in ns_data_list:
                if ((row[5] is '' or 'E-mail' in row[5])
                        and ('MINISTERSTWO' not in row[2])):
                    cfile.writerow(row)
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
