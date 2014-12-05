#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#


from __future__ import print_function
import os
from lxml import etree
import argparse

XSNS = {'xs': 'http://menis.gov.pl/sio/xmlSchema'}

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to xml files")
parser.add_argument("--rspo", help="no rspo", action="store_true")
parser.add_argument("--nomail", help="no mail", action="store_true")
parser.add_argument("--all", help="all", action="store_true")
args = parser.parse_args()


def xs(s):
    if s is None:
        return ''
    return unicode(s).encode('utf8')


def lista(i, a):
    lista = [
        xs(i.get('nrRspo')),
        "'" + xs(i.get('regon')),
        xs(i.get('pow')),
        xs(i.get('gm')),
        xs(i.get('typJed')),
        xs(i.get('nazwa')),
        xs(a.get('email')),
        xs(a.get('telefon')),
        xs(a.get('nazwaMiejsc')),
        "'" + xs(a.get('ulica')),
        "'" + xs(a.get('nrDomu')),
        xs(a.get('kodPoczt')),
        xs(a.get('poczta')),
        xs(i.get('nazwaOrganuProw')),
        xs(i.get('orgWydPow')),
        xs(i.get('orgWydGm')),
        xs(a.get('emailKomorki'))
    ]
    return lista


def out_dane(dane, file):
    file.write('\t'.join(dane) + '\n')
    print('\t'.join(dane))


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


def all_addresses(tree, file):
    i2s = tree.xpath('//i2a | //i2b | //i2c', namespaces=XSNS)
    for i in i2s:
        itree = etree.ElementTree(i)
        a = itree.xpath('//daneAdresowe', namespaces=XSNS)[0]
        l = lista(i, a)
        out_dane(l, file)


def set_header(file):
        file.write('\t'.join(
            ('RSPO',
             'REGON',
             'powiat',
             'gmina',
             'typ',
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
             'email kom.\n',)
        ))


os.system('clear')

if args.rspo:
    file = open('no_rspo.txt', 'w')
elif args.nomail:
    file = open('no_mail.txt', 'w')
elif args.all:
    file = open('all_addresses.txt', 'w')
else:
    exit("No required option...")
set_header(file)
for root, dirs, files in os.walk(args.path):
    for f in files:
        if f.endswith('.xml'):
            ff = os.path.join(root, f)
            tree = etree.parse(ff)
            if args.rspo:
                no_rspo(tree, file)
            elif args.nomail:
                no_email(tree, file)
            elif args.all:
                all_addresses(tree, file)
file.close()
