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
parser.add_argument("oldpath", help="path to DIR with OSIO XML files")
parser.add_argument('newpath', help='path to DIR with NSIO XLS files')
parser.add_argument("--ns-nomails", help="NSIO: no mails", action="store_true")
parser.add_argument("--ns-all", help="NSIO: all items", action="store_true")

args = parser.parse_args()


def find_duplicates(mylist):
    return [k for k, v in Counter(mylist).items() if v > 1]


def list_ids(wpath, id):
    listids = []
    for root, dirs, files in os.walk(wpath):
        for f in files:
            if f.endswith('.xml'):
                ff = os.path.join(root, f)
                tree = etree.parse(ff)
                i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
                for i in i2s:
                    if i.get(id):
                        listids.append(i.get(id))
    return listids


def xs(s):
    if s is None:
        return ''
    return unicode(s).encode('utf8')


def xi(s):
    if s is None:
        return 0
    return int(s)


def lista(i, a):
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
        xs(i.get('orgWydPow')),
        xs(i.get('orgWydGm')),
        xs(a.get('emailKomorki'))
    ]
    return lista


def out_dane(dane, file):
    file.writerow(dane)


def no_rspo(tree, file):
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        if i.get('nrRspo') is None and int(i.get('typJed')) < 101:
            l = lista(i, a)
            out_dane(l, file)


def no_email(tree, file):
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        if a.get('email') is None:
            l = lista(i, a)
            out_dane(l, file)


def all_items(tree, file):
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        l = lista(i, a)
        out_dane(l, file)


def set_header(file):
    naglowki = [
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
        'kod pow. org. wyd.',
        'kod gm. org. wyd.',
        'email kom.'
        ]
    file.writerow(naglowki)


def print_duplicates(dlist, tree, file, id):
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        if i.get(id) in dlist:
            l = lista(i, a)
            out_dane(l, file)


def get_ns_data(path):
    tree = etree.parse(os.path.join(path, '000038.xls'))
    nsTRspos = tree.xpath('//ss:Cell[@ss:Index="1"]/ss:Data/text()',
                          namespaces=XLSNS)
    nsTRegons = tree.xpath('//ss:Cell[@ss:Index="9"]/ss:Data/text()',
                           namespaces=XLSNS)
    nsTTyp = tree.xpath('//ss:Cell[@ss:Index="2"]/ss:Data/text()',
                        namespaces=XLSNS)
    nsTNames = tree.xpath('//ss:Cell[@ss:Index="3"]/ss:Data/text()',
                          namespaces=XLSNS)
    nsTOrgRej = tree.xpath('//ss:Cell[@ss:Index="6"]/ss:Data/text()',
                           namespaces=XLSNS)
    nsEmails = tree.xpath('//ss:Cell[@ss:Index="21"]/ss:Data',
                          namespaces=XLSNS)
    nsDRozDzi = tree.xpath('//ss:Cell[@ss:Index="34"]/ss:Data/text()',
                           namespaces=XLSNS)
    data = zip(nsTRspos, nsTRegons, nsTTyp, nsTNames, nsTOrgRej, nsEmails,
               nsDRozDzi)
    return data


def list_ns_ids(path, id):
    tree = etree.parse(os.path.join(path, '000038.xls'))
    print('*** ' + tree.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                              namespaces=XLSNS)[0])
    l = tree.xpath('//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
                   namespaces=XLSNS)
    treez = etree.parse(os.path.join(path, '000038z.xls'))
    print('*** ' + treez.xpath('//ss:Row[2]/ss:Cell/ss:Data/text()',
                               namespaces=XLSNS)[0])
    if id == '9':
        id = '10'
    lz = treez.xpath('//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
                     namespaces=XLSNS)
    return l + lz


def find_ns_no_mails(path):
    print('*** NS: no e-mails ***')
    data = get_ns_data(path)
    with open('ns_no_emails.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        for i, j, k, l, m, n, o in data:
                if n.text is None or 'E-mail':
                    print(i, j, len(j), k, l, m, n.text)
                    csvf.writerow([i, j, len(j), xs(k), xs(l), xs(m),
                                  n.text, xs(o)])


def ns_all_items(path):
    print('*** NS: all items ***')
    data = get_ns_data(path)
    with open('ns_all_items.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        for i, j, k, l, m, n, o in data:
                print(i, j, len(j), k, l, m, n.text, o)
                try:
                    csvf.writerow([xi(i), j, len(j), xs(k), xs(l), xs(m),
                                  n.text, xs(o)])
                except:
                    csvf.writerow([i, j, len(j), xs(k), xs(l), xs(m),
                                  n.text, xs(o)])

os.system('clear')

print('*** OS: Missing REGONs existing in NSIO with start earlier than ' +
      str(BORDER_DATE) + ' ***')
missing_regons = []
os_regons = list_ids(args.oldpath, 'regon')
ns_tree = etree.parse(os.path.join(args.newpath, '000038.xls'))
ns_regons = ns_tree.xpath(
    '//ss:Cell[@ss:Index="9"]/ss:Data/text()', namespaces=XLSNS
)
for i in ns_regons:
    if len(i) == 9:
        i = i + '00000'
    if i not in os_regons:
        missing_regons.append(i)
data = get_ns_data(args.newpath)
with open('brakujace_nr_regon.csv', 'wb') as f:
    csvf = csv.writer(f, delimiter=";", quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)
    for i, j, k, l, m, n, o in data:
        if len(j) == 9:
            j = j + '00000'
        try:
            odate = datetime.strptime(o, '%Y-%m-%d')
        except:
            odate = datetime.strptime('9999-01-01', '%Y-%m-%d')
        if (j in missing_regons and 'MINISTERSTWO' not in m and
                odate < BORDER_DATE) or i == 'Nr RSPO':
            try:
                csvf.writerow([xi(i), j, len(j), xs(k), xs(l), xs(m),
                              n.text, xs(o)])
            except:
                csvf.writerow([i, j, len(j), xs(k), xs(l), xs(m),
                              n.text, xs(o)])

print('*** OS: bad REGONs ***')
bad_regons = []
os_regons = list_ids(args.oldpath, 'regon')
ns_regons = list_ns_ids(args.newpath, '9')
for i in ns_regons:
    if len(i) == 9:
        ns_regons[ns_regons.index(i)] = i + '00000'
for i in os_regons:
    if i not in ns_regons:
        bad_regons.append(i)
with open('niepoprawne_numery_regon.csv', 'wb') as f:
    csvf = csv.writer(f, delimiter=";", quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)
    set_header(csvf)
    for root, dirs, files in os.walk(args.oldpath):
        for f in files:
            if f.endswith('.xml'):
                ff = os.path.join(root, f)
                tree = etree.parse(ff)
                i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
                for i in i2s:
                    itree = etree.ElementTree(i)
                    a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
                    if (i.get('regon') in bad_regons and
                            i.get('nrRspo') is not None):
                        csvf.writerow(lista(i, a))

print('*** OS: bad RSPOs ***')
bad_rspos = []
os_rspos = list_ids(args.oldpath, 'nrRspo')
ns_rspos = list_ns_ids(args.newpath, '1')
for i in os_rspos:
    if i not in ns_rspos:
        bad_rspos.append(i)
with open('niepoprawne_numery_rspo.csv', 'wb') as f:
    csvf = csv.writer(f, delimiter=";", quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)
    set_header(csvf)
    for root, dirs, files in os.walk(args.oldpath):
        for f in files:
            if f.endswith('.xml'):
                ff = os.path.join(root, f)
                tree = etree.parse(ff)
                i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
                for i in i2s:
                    itree = etree.ElementTree(i)
                    a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
                    if i.get('nrRspo') in bad_rspos:
                        csvf.writerow(lista(i, a))
if args.ns_nomails:
    find_ns_no_mails(args.newpath)
if args.ns_all:
    ns_all_items(args.newpath)

print('*** OS: duplicate REGONs ***')
dfb = open('zdublowane_regony.csv', 'wb')
dregonf = csv.writer(dfb, delimiter=";", quotechar='"',
                     quoting=csv.QUOTE_NONNUMERIC)
regons = list_ids(args.oldpath, 'regon')
dregons = find_duplicates(regons)
set_header(dregonf)

print('*** OS: duplicate RSPOs ***')
drb = open('zdublowane_nr_rspo.csv', 'wb')
drspof = csv.writer(drb, delimiter=";", quotechar='"',
                    quoting=csv.QUOTE_NONNUMERIC)
rspos = list_ids(args.oldpath, 'nrRspo')
drspos = find_duplicates(rspos)
set_header(drspof)

print('*** OS: no RSPOs ***')
nrb = open('brak_nr_rspo.csv', 'wb')
norspof = csv.writer(nrb, delimiter=";", quotechar='"',
                     quoting=csv.QUOTE_NONNUMERIC)
set_header(norspof)

print('*** OS: no e-mails ***')
nmf = open('brak_adresu_email.csv', 'wb')
nomailf = csv.writer(nmf, delimiter=";", quotechar='"',
                     quoting=csv.QUOTE_NONNUMERIC)
set_header(nomailf)

print('*** OS: all items ***')
allfb = open('all_items.csv', 'wb')
allf = csv.writer(allfb, delimiter=";", quotechar='"',
                  quoting=csv.QUOTE_NONNUMERIC)
set_header(allf)

for root, dirs, files in os.walk(args.oldpath):
    for f in files:
        if f.endswith('.xml'):
            ff = os.path.join(root, f)
            tree = etree.parse(ff)
            print_duplicates(dregons, tree, dregonf, 'regon')
            print_duplicates(drspos, tree, drspof, 'nrRspo')
            no_rspo(tree, norspof)
            no_email(tree, nomailf)
            all_items(tree, allf)
dfb.close()
drb.close()
nrb.close()
nmf.close()
allfb.close()
