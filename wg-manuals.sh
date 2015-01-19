#!/bin/bash
rm -r ~/cie_pdf/*.pdf
wget --no-clobber --convert-links -r -p -E -e robots=off -U mozilla -A pdf -nd -P ~/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/251-instrukcje-techniczne-do-obslugi-programu 
wget --no-clobber --convert-links -r -p -E -e robots=off -U mozilla -A pdf -nd -P ~/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/357-strefa-dla-zalogowanych
wget --no-clobber --convert-links -r -p -E -e robots=off -U mozilla -A pdf -nd -P ~/cie_pdf http://sio.men.gov.pl/index.php/pomoc/instrukcje-uzytkownika/245-komentarze-merytoryczne-do-instrukcji-uzytkownika