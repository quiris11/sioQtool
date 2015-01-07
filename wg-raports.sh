#!/bin/bash
read -p "Username: " UNAME
read -s -p "Password: " PASSWD
wget --delete-after --keep-session-cookies --save-cookies=my_cookies.txt --post-data="nazwaUzytkownika=$UNAME&hasloUzytkownika=$PASSWD&param=Start_login" https://sio.men.gov.pl/dodatki/strefa/index.php
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_6 --output-document=$HOME/NSIO/rspo_active.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_65 --output-document=$HOME/NSIO/rspo_inactive.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_61 --output-document=$HOME/NSIO/ee_przedszk.xls
wget --load-cookies=my_cookies.txt https://sio.men.gov.pl/dodatki/strefa/index.php?param=Support_download_62 --output-document=$HOME/NSIO/ee_sp.xls
rm my_cookies.txt
