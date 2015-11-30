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

from conf import ERROR_SOUND, SUCCESS_SOUND, URL, UA


class BadResponseError(Exception):
    pass


def play_success():
    os.system('paplay {}'.format(SUCCESS_SOUND))


def play_error():
    os.system('paplay {}'.format(ERROR_SOUND))


def do_check():
    headers = {
        'User-Agent': UA,
    }
    r = requests.get(URL, headers=headers)
    if not r.status_code == 200:
        raise BadResponseError
    pq = pyquery.PyQuery(r.content)
    tables = pq.find('.calendar-month-table table')
    available_dates = tables.find('td.buchbar')
    if available_dates.length:
        play_success()
    else:
        print('No dates, skipping')


def get_delay():
    return random.randint(100, 300)


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
