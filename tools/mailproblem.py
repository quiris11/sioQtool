#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#


def mail_problem(csvf, params):
    import smtplib
    import csv
    import imp
    import sys
    from email.mime.text import MIMEText
    from email.header import Header

    def get_vars(params):
        with open(params) as f:
            data = imp.load_source('data', '', f)
        return data

    data = get_vars(params)

    def mail(msg, data):
        server = smtplib.SMTP(data.SMTP_SERVER)
        server.sendmail(data.FROM_ADDRESS, data.TO_ADDRESS, msg.as_string())
        server.quit()

    with open(csvf) as f:
        for row in csv.reader(f, delimiter=';', quotechar='"'):
            # print(row)
            # print(row[0])
            content = 'Szanowni Państwo,\n\n'
            content += \
                'Analiza danych zgromadzonych w dwóch systemach informacji ' \
                'oświatowej (starym SIO i nowym SIO) wykazała istnienie ' \
                'poważnego ' \
                'problemu w szkole/placówce o następujących danych ' \
                'identyfikacyjnych:\n\n' \
                'REGON: ' + row[4] + ' \n' \
                'Nr RSPO: ' + row[3] + ' \n' \
                'Nazwa: ' + row[10] + ' \n\n' \
                'Problem polega na niezgodności danych pomiędzy dwoma ' \
                'systemami SIO w następującym obszarze:\n\n' \
                ' '
            content += '\n\n-- \n' + data.SIGNED

            msg = MIMEText(content, 'plain', 'utf-8')
            msg['To'] = data.TO_ADDRESS
            msg['From'] = data.FROM_ADDRESS
            msg['Subject'] = Header('Test - zażółć gęślą jaźń', 'utf-8')
            # print content
            # print msg.as_string()

            # mail(msg, data)
if __name__ == '__main__':
    mail_problem('!critical!/osn_niepoprawne_pole_publicznosc.csv', 'smtp.txt')
