#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import contextlib
import logging
import os
import platform
import random
import time
import traceback

import signal
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities

from conf import ERROR_SOUND, SUCCESS_SOUND, URL, UA, DRIVER, BASE_DIR

logging.basicConfig()
log = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)
log.setLevel(logging.INFO)


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


def get_driver(driver_name=None):
    _driver_name = driver_name or DRIVER
    if _driver_name == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "whatever you want")
        driver = webdriver.Firefox(profile)
        driver.set_window_size(1280, 1024)
        return driver
    elif _driver_name == 'phantomjs':
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = UA
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1280, 1024)
        return driver
    else:
        raise Exception("bad DRIVER value: %s" % DRIVER)


@contextlib.contextmanager
def driver_mgr(driver_name=None):
    driver = get_driver(driver_name)
    try:
        yield driver
    finally:
        if DRIVER == 'phantomjs':
            # See https://github.com/SeleniumHQ/selenium/issues/767
            driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()


def get_name():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def log_page(driver):
    basename = get_name()
    source_name = os.path.join(
        BASE_DIR,
        'screens',
        basename + '.html'
    )
    screen_name = os.path.join(
        BASE_DIR,
        'screens',
        basename + '.png'
    )
    with open(source_name, 'w+') as source_file:
        source_file.write(driver.page_source.encode('utf-8'))
    driver.get_screenshot_as_file(screen_name)


def get_click_delay():
    return random.randint(3, 10)


def do_check(driver):
    assert isinstance(driver, (webdriver.Firefox, webdriver.PhantomJS))
    tables = driver.find_elements_by_css_selector('.calendar-month-table table')
    for table in tables:
        available_dates = table.find_elements_by_css_selector('td.buchbar')
        if available_dates:
            log_page(driver)
            filtered_dates = []
            for a_date in available_dates:
                day = a_date.text
                day = int(day)
                # if day not in (28, 29, 30):
                filtered_dates.append(day)
            if filtered_dates:
                play_success()
                log.info("Available dates: %s", ", ".join(map(str, filtered_dates)))
            else:
                log.info('No dates, skipping')
            for some_date in available_dates:
                link = some_date.find_element_by_css_selector('a')
                href = link.get_attribute('href')
                log.info("Applying for date: %s at url %s", some_date.text, href)
                time.sleep(get_click_delay())
                link.click()
                log_page(driver)
                timetable = driver.find_element_by_css_selector(".calendar-table .timetable")
                try:
                    rows = timetable.find_element_by_css_selector("table tbody tr")
                except NoSuchElementException:
                    driver.back()
                    continue
                available_times = []
                for row in rows:
                    try:
                        time_el = row.find_element_by_css_selector("th.buchbar")
                        link_el = row.find_element_by_css_selector("td.frei a")
                    except NoSuchElementException:
                        continue
                    log.info("Time %s at %s", time_el.text, link_el.text)
                    available_times.append((time_el, link_el))
                if available_times:
                    time.sleep(get_click_delay())
                    available_times[0][1].click()
                    log_page(driver)
                driver.back()
            return True
        else:
            log.info('No dates, skipping')
    return False


def get_refresh_delay():
    return random.randint(60, 200)


def main():
    error_coeff = 1
    with driver_mgr() as driver:
        driver.get(URL)
        while True:
            try:
                do_get = do_check(driver)
            except BadResponseError:
                error_coeff += 1
                delay = get_refresh_delay() * error_coeff
                do_get = True
            except Exception:
                print("Abnormal error:")
                traceback.print_exc()
                error_coeff += 1
                delay = get_refresh_delay() * error_coeff
                do_get = True
            else:
                error_coeff = 1
                delay = get_refresh_delay()
            time.sleep(delay)
            if do_get:
                driver.get(URL)
            else:
                driver.refresh()


if __name__ == '__main__':
    main()
