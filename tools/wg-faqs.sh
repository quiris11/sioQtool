#!/bin/bash
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#
mkdir "$HOME/cie_faqs"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=d2130071daf3ac8b056c519676c170c6&searchMode=undefined" --output-document="$HOME/cie_faqs/Dane zbiorcze.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=75f530437b42e0aaa0a1f47464b1c532&searchMode=undefined" --output-document="$HOME/cie_faqs/Instalacja aplikacji.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=f8efee67d2f31c13af12c477c53a59d3&searchMode=undefined" --output-document="$HOME/cie_faqs/Jednostki pozarejestrowe.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=3626b333b7f28d6a45020d95d6b7b56a&searchMode=undefined" --output-document="$HOME/cie_faqs/Logowanie Reset hasła.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=97284232a4b135ede6961ac90cc88c94&searchMode=undefined" --output-document="$HOME/cie_faqs/Nauczyciel.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=29cce7c8e6b7c7177c7af982038d5d23&searchMode=undefined" --output-document="$HOME/cie_faqs/Podmiot.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=533e2332623ad9c93e5a3bd56f93c8af&searchMode=undefined" --output-document="$HOME/cie_faqs/Praca z aplikacją.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=f6f8005c3b7549db834e2c0c6972c91f&searchMode=undefined" --output-document="$HOME/cie_faqs/RSPO.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=4ec64997463410d36630e037939875c6&searchMode=undefined" --output-document="$HOME/cie_faqs/Sprawozdawczość i statystyka.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=423d2ab72b00b1e3a0b295d3e757fa86&searchMode=undefined" --output-document="$HOME/cie_faqs/Strefa dla zalogowanych.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=58806385b55f0ae7214b1528880cdb6f&searchMode=undefined" --output-document="$HOME/cie_faqs/Uczeń.html"
wget http://sio.men.gov.pl/dodatki/sio2_support/index.php --post-data "param=Support_htmlContent&phrase=&category=d5468199a76795f7842aa9b837fcffe0&searchMode=undefined" --output-document="$HOME/cie_faqs/Wnioski o nadanie upoważnienia.html"
