# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import platform

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

UA = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

SUCCESS_SOUND_LINUX = os.path.join(BASE_DIR, 'tada.ogg')
ERROR_SOUND_LINUX = os.path.join(BASE_DIR, 'alarm.ogg')
SUCCESS_SOUND_MAC = os.path.join(BASE_DIR, 'tada.wav')
ERROR_SOUND_MAC = os.path.join(BASE_DIR, 'alarm.wav')

if platform.system() == 'Darwin':
    SUCCESS_SOUND = SUCCESS_SOUND_MAC
    ERROR_SOUND = ERROR_SOUND_MAC
else:
    SUCCESS_SOUND = SUCCESS_SOUND_LINUX
    ERROR_SOUND = ERROR_SOUND_LINUX


URL = 'https://service.berlin.de/terminvereinbarung/termin/tag.php?id=&buergerID=&buergername=&absagecode=&Datum=1456786800&anliegen%5B%5D=120686&dienstleister%5B%5D=122210&dienstleister%5B%5D=122217&dienstleister%5B%5D=122219&dienstleister%5B%5D=122227&dienstleister%5B%5D=122231&dienstleister%5B%5D=122238&dienstleister%5B%5D=122243&dienstleister%5B%5D=122252&dienstleister%5B%5D=122260&dienstleister%5B%5D=122262&dienstleister%5B%5D=122254&dienstleister%5B%5D=122271&dienstleister%5B%5D=122273&dienstleister%5B%5D=122277&dienstleister%5B%5D=122280&dienstleister%5B%5D=122282&dienstleister%5B%5D=122284&dienstleister%5B%5D=122291&dienstleister%5B%5D=122285&dienstleister%5B%5D=122286&dienstleister%5B%5D=122296&dienstleister%5B%5D=150230&dienstleister%5B%5D=122301&dienstleister%5B%5D=122297&dienstleister%5B%5D=122294&dienstleister%5B%5D=122312&dienstleister%5B%5D=122314&dienstleister%5B%5D=122304&dienstleister%5B%5D=122311&dienstleister%5B%5D=122309&dienstleister%5B%5D=317869&dienstleister%5B%5D=324433&dienstleister%5B%5D=325341&dienstleister%5B%5D=324434&dienstleister%5B%5D=324435&dienstleister%5B%5D=122281&dienstleister%5B%5D=324414&dienstleister%5B%5D=122283&dienstleister%5B%5D=122279&dienstleister%5B%5D=122276&dienstleister%5B%5D=122274&dienstleister%5B%5D=122267&dienstleister%5B%5D=122246&dienstleister%5B%5D=122251&dienstleister%5B%5D=122257&dienstleister%5B%5D=122208&dienstleister%5B%5D=122226&herkunft=/terminvereinbarung/'


