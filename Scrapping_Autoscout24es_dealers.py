# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:22:35 2021

@author: c02662
"""

# Importation des modules perso
from datetime import datetime , timedelta, date

import time
from random import randint
import pandas as pd
import sys

from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_TIME, "fr") 
import os
sys.path.append(os.path.abspath("//FRSHARES0479.france.intra.corp/Corporate_Remarketing/Remarketing_Data_Intelligence/200_MARKET_INTELLIGENCE/210_WEBSCRAPPING/213_SCRAPPING/"))
import Scrapping_def


user = "c02662"
password = "XSL-Mcosmic4000"
# Test du User/password
url = "https://www.google.fr/"
test = Scrapping_def.proxy_test(user, password,url)



import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

proxies  = {"http":"http://{user}:{pwd}@primaryprx.intra.corp:8090".format(user=user,pwd=password),"https":"http://{user}:{pwd}@primaryprx.intra.corp:8090".format(user=user,pwd=password)}
print(proxies)

url = "https://profesionales.autoscout24.es/DealersSearch/Find"

dealers = []
for elm in range(1,32):
    try:
        payload={"CurrentPage":elm,"ResultsPerPage":100}
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload,proxies = proxies, verify  = False)
        # print(response.text)
        dealers.extend(response.json()['dealers'])
    except:
        pass
dealers = json_normalize(dealers)

dealer_list = dealers["UrlName"][876:].tolist()

Json_dataframe = pd.DataFrame()
j=0
for i in dealer_list:
    j = j+1
    if j % 3 == 0:
        time.sleep(randint(2, 3))
    print(str(j) + " - " + str(i))
    url = "https://www.autoscout24.es/profesionales/{}?srcl=2&intpgat=dealersearch-home&ipc=dealersearch%7Cdealerinfo&ipl=result".format(i)
    print(url)
    soup_mysite = Scrapping_def.DOM_extract(user , password, url, chrome = False, sleep = False)
    test = soup_mysite.find("script",{"id":"initial-state"}).contents[0]
    Json_dftp = json_normalize(json.loads(test)["dealerInfoPage"])
    Json_dataframe = Json_dataframe.append(Json_dftp)

Json_dataframe_271 = Json_dataframe
Json_dataframe_606 = Json_dataframe
Json_dataframe_876 = Json_dataframe


    
dealers.to_excel('//FRSHARES0479.france.intra.corp/Corporate_Remarketing/Remarketing_Data_Intelligence/200_MARKET_INTELLIGENCE/210_WEBSCRAPPING/213_SCRAPPING/dealers_es.xlsx')
