#!/bin/bash
#
# This file is part of sioQtool, licensed under GNU Affero GPLv3 or later.
# Copyright © Robert Błaut. See NOTICE for more information.
#
wget --no-clobber --convert-links -N -r -p -E -e robots=off -U mozilla -A pdf -nd -P $HOME/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/251-instrukcje-techniczne-do-obslugi-programu
wget --no-clobber --convert-links -N -r -p -E -e robots=off -U mozilla -A pdf -nd -P $HOME/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/357-strefa-dla-zalogowanych
wget --no-clobber --convert-links -N -r -p -E -e robots=off -U mozilla -A pdf -nd -P $HOME/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/245-komentarze-merytoryczne-do-instrukcji-uzytkownika
