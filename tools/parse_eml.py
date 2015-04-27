#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#

import os
import csv
from email.Parser import Parser
from email.utils import parseaddr
from email.Header import decode_header

path = os.path.join(os.path.expanduser("~"), 'eml')
p = Parser()
idmails = []
for root, dirs, files in os.walk(path):
    for single_file in files:
        if single_file.endswith('.eml'):
            with open(os.path.join(root, single_file)) as f:
                msgobj = p.parse(f)
                for part in msgobj.walk():
                    content_disposition = part.get("Content-Disposition", None)
                    if content_disposition:
                        dispositions = content_disposition.strip().split(";")
                        if bool(
                            content_disposition and
                            dispositions[0].lower() == "attachment"
                        ):
                            for param in dispositions[1:]:
                                if 'filename' in param:
                                    name, value = param.split("=", 1)
                                    bytes, encoding = decode_header(
                                        value.replace('"', '')
                                    )[0]
                                    if encoding is not None:
                                        decoded = bytes.decode(encoding)
                                        if bytes.decode(encoding).endswith(
                                            '103.exp'
                                        ):
                                            idmails.append([
                                                bytes.decode(encoding)[:-4],
                                                parseaddr(msgobj.get(
                                                    'From'
                                                ))[1]
                                            ])
                                    else:
                                        if bytes.endswith('.exp'):
                                            idmails.append([
                                                bytes[:-4],
                                                parseaddr(msgobj.get(
                                                    'From'
                                                ))[1]
                                            ])
with open(os.path.join('NSIO', 'jsts_dict.txt'), 'r') as f:
    jst_dict = eval(f.read())
with open(os.path.join('NSIO', 'idmails.csv'), 'w') as o:
    csvwrite = csv.writer(o, delimiter=';', quotechar='"',
                          quoting=csv.QUOTE_NONNUMERIC)
    for r in idmails:
        try:
            csvwrite.writerow([r[0], jst_dict[r[0]], r[1]])
        except:
            csvwrite.writerow([r[0], '! problem', r[1]])
