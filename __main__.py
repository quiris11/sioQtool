#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

from __future__ import print_function
from lxml import etree
from collections import Counter
import argparse
import os
import csv
import sys

XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}
XLSNS = {'o': 'urn:schemas-microsoft-com:office:office',
         'x': 'urn:schemas-microsoft-com:office:excel',
         'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}

parser = argparse.ArgumentParser()
parser.add_argument("path", nargs='?', help="path to xml files")
parser.add_argument('-x', '--xls', nargs='?', metavar='DIR', default='',
                    help='path to DIR with NSIO xls files')
parser.add_argument("-S", "--norspo", help="no rspo", action="store_true")
parser.add_argument("-r", "--dregon", help="duplicate REGON",
                    action="store_true")
parser.add_argument("-s", "--drspo", help="duplicate RSPO",
                    action="store_true")
parser.add_argument("-m", "--nomail", help="no mail", action="store_true")
parser.add_argument("-a", "--all", help="all", action="store_true")
parser.add_argument("-A", "--ns-all", help="all in NSIO", action="store_true")
parser.add_argument("-M", "--ns-nomail", help="no mail in NSIO",
                    action="store_true")
parser.add_argument("-b", "--bad-rspo", help="bad RSPO in OSIO",
                    action="store_true")
parser.add_argument("-B", "--bad-regon", help="bad REGON in OSIO",
                    action="store_true")
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
    # file.write('\t'.join(dane) + '\n')
    file.writerow(dane)
    # print('\t'.join(dane))


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
    data = zip(nsTRspos, nsTRegons, nsTTyp, nsTNames, nsTOrgRej, nsEmails)
    return data


def list_ns_ids(path, id):
    tree = etree.parse(os.path.join(path, '000038.xls'))
    l = tree.xpath('//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
                   namespaces=XLSNS)
    treez = etree.parse(os.path.join(path, '000038z.xls'))
    if id == '9':
        id = '10'
    lz = treez.xpath('//ss:Cell[@ss:Index="' + id + '"]/ss:Data/text()',
                     namespaces=XLSNS)
    # print(l + lz)
    return l + lz


def find_ns_no_mails(path):
    print('*** NS: no Emails ***')
    data = get_ns_data(path)
    with open('ns_no_emails.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        for i, j, k, l, m, n in data:
                if n.text is None or 'E-mail':
                    print(i, j, len(j), k, l, m, n.text)
                    csvf.writerow([i, j, len(j), xs(k), xs(l), xs(m),
                                  n.text])


def ns_all_items(path):
    print('*** NS: All items ***')
    data = get_ns_data(path)
    with open('ns_all_items.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        for i, j, k, l, m, n in data:
                print(i, j, len(j), k, l, m, n.text)
                try:
                    csvf.writerow([xi(i), j, len(j), xs(k), xs(l), xs(m),
                                  n.text])
                except:
                    csvf.writerow([i, j, len(j), xs(k), xs(l), xs(m),
                                  n.text])

os.system('clear')
if args.bad_regon:
    print('*** OS: bad REGON ***')
    bad_regons = []
    os_regons = list_ids(args.path, 'regon')
    ns_regons = list_ns_ids(args.xls, '9')
    for i in ns_regons:
        if len(i) == 9:
            ns_regons[ns_regons.index(i)] = i + '00000'
    # print(ns_regons)
    for i in os_regons:
        if i not in ns_regons:
            bad_regons.append(i)
    # print(bad_regons)
    with open('niepoprawne_numery_regon.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        set_header(csvf)
        for root, dirs, files in os.walk(args.path):
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
if args.bad_rspo:
    print('*** OS: bad RSPO ***')
    bad_rspos = []
    os_rspos = list_ids(args.path, 'nrRspo')
    ns_rspos = list_ns_ids(args.xls, '1')
    for i in os_rspos:
        if i not in ns_rspos:
            bad_rspos.append(i)
    # print(bad_rspos)
    with open('niepoprawne_numery_rspo.csv', 'wb') as f:
        csvf = csv.writer(f, delimiter=";", quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
        set_header(csvf)
        for root, dirs, files in os.walk(args.path):
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
if args.ns_nomail:
    find_ns_no_mails(args.xls)
if args.ns_all:
    ns_all_items(args.xls)
if args.dregon:
    print('*** OS: duplicate REGON ***')
    dfb = open('zdublowane_regony.csv', 'wb')
    dregonf = csv.writer(dfb, delimiter=";", quotechar='"',
                         quoting=csv.QUOTE_NONNUMERIC)
    regons = list_ids(args.path, 'regon')
    dregons = find_duplicates(regons)
    set_header(dregonf)
if args.drspo:
    print('*** OS: duplicate RSPO ***')
    drb = open('zdublowane_nr_rspo.csv', 'wb')
    drspof = csv.writer(drb, delimiter=";", quotechar='"',
                        quoting=csv.QUOTE_NONNUMERIC)
    rspos = list_ids(args.path, 'nrRspo')
    drspos = find_duplicates(rspos)
    set_header(drspof)
if args.norspo:
    print('*** OS: no RSPO ***')
    nrb = open('brak_nr_rspo.csv', 'wb')
    norspof = csv.writer(nrb, delimiter=";", quotechar='"',
                         quoting=csv.QUOTE_NONNUMERIC)
    set_header(norspof)
if args.nomail:
    print('*** OS: no e-mail ***')
    nmf = open('brak_adresu_email.csv', 'wb')
    nomailf = csv.writer(nmf, delimiter=";", quotechar='"',
                         quoting=csv.QUOTE_NONNUMERIC)
    set_header(nomailf)
if args.all:
    print('*** All items ***')
    allfb = open('all_items.csv', 'wb')
    allf = csv.writer(allfb, delimiter=";", quotechar='"',
                      quoting=csv.QUOTE_NONNUMERIC)
    set_header(allf)
if args.path:
    for root, dirs, files in os.walk(args.path):
        for f in files:
            if f.endswith('.xml'):
                ff = os.path.join(root, f)
                tree = etree.parse(ff)
                if args.dregon:
                    print_duplicates(dregons, tree, dregonf, 'regon')
                if args.drspo:
                    print_duplicates(drspos, tree, drspof, 'nrRspo')
                if args.norspo:
                    no_rspo(tree, norspof)
                if args.nomail:
                    no_email(tree, nomailf)
                if args.all:
                    all_items(tree, allf)
    try:
        dfb.close()
    except:
        pass
    try:
        drb.close()
    except:
        pass
    try:
        nrb.close()
    except:
        pass
    try:
        nmf.close()
    except:
        pass
    try:
        allfb.close()
    except:
        pass
