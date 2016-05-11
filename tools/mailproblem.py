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
        # server.sendmail(data.FROM_ADDRESS, [row[13], row[14]], msg.as_string())  # Be cafeful !!!
        # server.sendmail(data.FROM_ADDRESS, data.TO_ADDRESS, msg.as_string())  # Be cafeful !!!
        server.quit()

    with open(csvf) as f:
        counter = 0
        for row in csv.reader(f, delimiter=',', quotechar='"'):
            counter += 1
            # if counter == 30:
            #     sys.exit()
            if '@' not in row[13]:
                continue
            print(row[11], row[12], row[13], row[14])
            content = 'Szanowni Państwo,\n\n' \
                'Wszelkie pytania proszę kierować do:\n' \
                '\n\n-- \n%s' % (row[11], row[12], data.SIGNED)
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['To'] = row[13]
            msg['CC'] = row[14]
            msg['From'] = data.FROM_ADDRESS
            msg['Subject'] = Header('Dane do logowania w sytemie „Dotacje”',
                                    'utf-8')
            # print content
            mail(msg, data)

if __name__ == '__main__':
    mail_problem('dotacje.csv', 'Dropbox/smtp.txt')
