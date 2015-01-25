#!/bin/bash
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#
read -p "Username: " UNAME
read -s -p "Password: " PASSWD
wget --delete-after --keep-session-cookies --save-cookies=my_cookies.txt --post-data="nazwaUzytkownika=$UNAME&hasloUzytkownika=$PASSWD&param=Start_login" https://sio.men.gov.pl/dodatki/strefa/index.php
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_6 --output-document=$HOME/NSIO/rspo_aktywne.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_65 --output-document=$HOME/NSIO/rspo_nieaktywne.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_61 --output-document=$HOME/NSIO/ee_przedszk.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_62 --output-document=$HOME/NSIO/ee_sp.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_63 --output-document=$HOME/NSIO/obwody.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_64 --output-document=$HOME/NSIO/zawody.xls
rm my_cookies.txt
more ~/NSIO/rspo_nieaktywne.xls | grep ">Wykaz"