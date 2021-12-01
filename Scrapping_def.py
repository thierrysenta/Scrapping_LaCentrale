# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 18:34:47 2021

@author: c02662
"""

import logging
import os
import pandas as pd
import shutil
import sys
import time
import urllib.request

from bs4 import BeautifulSoup  # importation de la fonction BeautifulSoup dans le module bs4
from collections import OrderedDict
from datetime import datetime
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options

from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_TIME, "fr")
import urllib.request

import win32com.client as win32

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
import traceback
import msvcrt

import os


def proxy_test(user, password, url):
    try:
        url = url
        req = urllib.request
        url_proxy = r'http://{}:{}@primaryprx.intra.corp:8090'.format(user, password)
        proxy = req.ProxyHandler({'http': url_proxy, 'https': url_proxy})
        auth = req.HTTPBasicAuthHandler()
        opener = req.build_opener(proxy, auth, req.HTTPHandler)
        #opener.addheaders = [('User-agent',
        #                      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
        req.install_opener(opener)
        conn = req.urlopen(url)
        return conn.read()
        # scrAPI.conn_proxy(user, password, url)
    except OSError as e:
        if "authenticationrequired" in str(e.reason):
            print("Mauvais Username/password")
            sys.exit()
        else:
            sys.exit(e)


def get_chrome_driver(user, password):
    # Création du navigateur headless
    chrome_driver_path = "C:\\Users\\PC portable\\PycharmProjects\\Scrapping_LaCentrale\\chromedriver.exe"
    service_args = []
    service_args = [
        '--proxy=http://{}:{}@primaryprx.france.intra.corp:8090'.format(user, password),
        '--proxy-type=https']
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Cacher les logs de headless Chrome
    options.add_argument('log-level=3')
    options.add_argument('--disable-extensions')
    options.add_argument('--test-type')

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    capabilities['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

    return webdriver.Chrome(chrome_driver_path,
                            chrome_options=options,
                            service_args=service_args,
                            desired_capabilities=capabilities)


def DOM_extract(user, password, url, chrome=False, sleep=False, debug=False):
    if chrome:
        # print("chrome")
        driver = get_chrome_driver(user, password)
        # Ouverture du site par le navigateur
        driver.get(url)
        if sleep: time.sleep(5)
        # print("sleep 2s")
        # Récupération du code HTML de la page après execution du Javascript
        htmlSource = driver.page_source
        # Si debug n'est pas = à True, on ferme le navigateur headless
        if not debug:
            driver.close()
        else:
            return driver

    else:
        # Recupération du code HTML de la page "description détaillé" de la voiture
        htmlSource = proxy_test(user, password, url)
        # sans proxy :
        #htmlSource = urllib.request.urlopen(url).read()
    # Lecture du code HTML par le module Beautifulsoup
    return BeautifulSoup(htmlSource, "html.parser")    
    #return BeautifulSoup(htmlSource, "lxml")