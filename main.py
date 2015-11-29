#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import random
import time

import pyquery
import requests

from conf import SOUND, URL, UA


def play_sound():
    os.system('paplay {}'.format(SOUND))


def do_check():
    headers = {
        'User-Agent': UA,
    }
    r = requests.get(URL, headers=headers)
    if not r.status_code == 200:
        raise Exception('Bad response')
    pq = pyquery.PyQuery(r.content)
    tables = pq.find('.calendar-month-table table')
    available_dates = tables.find('td.buchbar')
    if available_dates.length:
        play_sound()
    else:
        print('No dates, skipping')


def main():
    while True:
        delay = random.randint(100, 300)
        do_check()
        time.sleep(delay)

if __name__ == '__main__':
    main()
