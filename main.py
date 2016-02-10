#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import platform
import random
import time

import pyquery
import requests

from conf import ERROR_SOUND, SUCCESS_SOUND, URL, UA


class BadResponseError(Exception):
    pass


def play_success_linux():
    os.system('paplay {}'.format(SUCCESS_SOUND))


def play_error_linux():
    os.system('paplay {}'.format(ERROR_SOUND))


def play_success_mac():
    os.system('afplay {}'.format(SUCCESS_SOUND))


def play_error_mac():
    os.system('afplay {}'.format(ERROR_SOUND))


if platform.system() == 'Darwin':
    play_success = play_success_mac
    play_error = play_error_mac
else:
    play_success = play_success_linux
    play_error = play_error_linux


def do_check():
    headers = {
        'User-Agent': UA,
    }
    r = requests.get(URL, headers=headers)
    if not r.status_code == 200:
        raise BadResponseError
    pq = pyquery.PyQuery(r.content)
    tables = pq.find('.calendar-month-table table')
    this_month_table = None
    for table in tables:
        _t = pyquery.PyQuery(table)
        month_name = _t.find('thead th.month').text().strip()
        if month_name.startswith('Februar'):
            this_month_table = _t
            break
    available_dates = this_month_table.find('td.buchbar')
    if available_dates.length:
        filtered_dates = []
        for a_date in available_dates:
            day = pyquery.PyQuery(a_date).text()
            day = int(day)
            # if day not in (28, 29, 30):
            filtered_dates.append(day)
        if filtered_dates:
            play_success()
            print(*filtered_dates, sep='\n')
        else:
            print('No dates, skipping')
    else:
        print('No dates, skipping')


def get_delay():
    return random.randint(60, 200)


def main():
    error_coeff = 1
    while True:
        try:
            do_check()
        except BadResponseError:
            error_coeff += 1
            delay = get_delay() * error_coeff
        else:
            error_coeff = 1
            delay = get_delay()
        time.sleep(delay)


if __name__ == '__main__':
    main()
