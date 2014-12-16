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

XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to xml files")
parser.add_argument("-S", "--norspo", help="no rspo", action="store_true")
parser.add_argument("-r", "--dregon", help="duplicate REGON",
                    action="store_true")
parser.add_argument("-s", "--drspo", help="duplicate RSPO",
                    action="store_true")
parser.add_argument("-m", "--nomail", help="no mail", action="store_true")
parser.add_argument("-a", "--all", help="all", action="store_true")
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


os.system('clear')

if args.dregon:
    print('*** Duplicate REGON ***')
    dfb = open('zduplikowane_regony.csv', 'wb')
    dregonf = csv.writer(dfb, delimiter=";", quotechar='"',
                         quoting=csv.QUOTE_NONNUMERIC)
    regons = list_ids(args.path, 'regon')
    dregons = find_duplicates(regons)
    set_header(dregonf)
if args.drspo:
    print('*** Duplicate RSPO ***')
    drb = open('zduplikowane_nr_rspo.csv', 'wb')
    drspof = csv.writer(drb, delimiter=";", quotechar='"',
                        quoting=csv.QUOTE_NONNUMERIC)
    rspos = list_ids(args.path, 'nrRspo')
    drspos = find_duplicates(rspos)
    set_header(drspof)
if args.norspo:
    print('*** No RSPO ***')
    nrb = open('brak_nr_rspo.csv', 'wb')
    norspof = csv.writer(nrb, delimiter=";", quotechar='"',
                         quoting=csv.QUOTE_NONNUMERIC)
    set_header(norspof)
if args.nomail:
    print('*** No e-mail ***')
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
# else:
    # exit("No required option...")
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
