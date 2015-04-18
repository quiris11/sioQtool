#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#


def transform(path, extension):
    import os
    import shutil
    import subprocess

    def unpack_exp(exp):
        subprocess.check_call([
            'java',
            '-jar',
            os.path.join(dekod_path, 'AnalizaPlikow.jar'),
            os.path.join(exp)
        ])

    home = os.path.expanduser("~")
    dekod_path = os.path.join(home, 'github/Dekod')
    if not os.path.exists(os.path.join('OSIO')):
        os.makedirs(os.path.join('OSIO'))

    if extension == '.krt':
        exp = os.path.join('OSIO.exp')
        shutil.rmtree(os.path.join('OSIO'))
        shutil.copyfile(os.path.join(path), exp)
        unpack_exp(exp)
        os.remove(exp)
    elif extension == '.exp':
        for root, dirs, files in os.walk(path):
            for single_file in files:
                if single_file.endswith('.exp'):
                    single_file_path = os.path.join(root, single_file)
                    shutil.copy(single_file_path, 'OSIO')
                    try:
                        print('* Unapacking EXP file: ' +
                              os.path.basename(single_file_path[:-4]))
                        shutil.rmtree(os.path.join(
                            'OSIO',
                            os.path.basename(single_file_path[:-4])
                        ))
                    except:
                        pass
                    unpack_exp(os.path.join(
                        'OSIO',
                        os.path.basename(single_file_path)
                    ))
                    os.remove(os.path.join(
                        'OSIO',
                        os.path.basename(single_file_path)
                    ))
