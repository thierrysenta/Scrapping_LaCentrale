# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:37:29 2019

@author: c02662
"""

# Importation des modules perso
from datetime import datetime, timedelta, date

import time
import pandas as pd
import sys

from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_TIME, "fr")
import os

sys.path.append(os.path.abspath(
    "//FRSHARES0479.france.intra.corp/Corporate_Remarketing/Remarketing_Data_Intelligence/200_MARKET_INTELLIGENCE/210_WEBSCRAPPING/213_SCRAPPING/"))
import Scrapping_def

user = "c02662"
password = "XSL-Mcosmic4000"
# Test du User/password
url = "https://www.google.fr/"
Scrapping_def.proxy_test(user, password, url)

page = 0
url = "https://www.lacentrale.fr/pro_list.php?rubrique=VEHICULES&num_page={}".format(page)
print(url)

soup_mysite = Scrapping_def.DOM_extract(user, password, url, chrome=True, sleep=True)

print(soup_mysite)

FileOut = "//FRSHARES0479.france.intra.corp/Corporate_Remarketing/MIT/10_EXTERNAL_DATA/01_WebScrapping/Python/extraction/LC/dealers/List_dealers_LaCentrale_20191312.csv"

soup_mysite = scrAPI.DOM_extract(user, password, url, chrome=False, sleep=False)
# print(soup_mysite)


## Nombre de dealers et nombre de pages :
nb_dealers = int(soup_mysite.find('h2', {"class": "NbResults floatL bold sizeC lH35 inlineBlock mR30"}).text.replace(
    "professionnels", "").replace("\n", "").replace(" ", "")) + 1
nb_pages = int(nb_dealers / 20) + 1
print("Nombre de dealers", nb_dealers)
print("Nombre de pages", nb_pages)

# En cas de test :
npage_deb = 1
nb_pages = 380

list_URL = []
list_VolAdds = []
for i in range(npage_deb, nb_pages + 1):
    url = "https://www.lacentrale.fr/pro_list.php?rubrique=VEHICULES&num_page={}".format(i)
    print("Page ", i, "URL :", url)
    soup_mysite = scrAPI.DOM_extract(user, password, url, chrome=False, sleep=False)
    ids = [x.find("a", {"class": "btnDark btnNbAd"})["href"] for x in
           soup_mysite.find_all("div", {"class": "itemListing pH10 hiddenOverflow"})]
    # print(ids)
    Volume_adds = [x.find("span", {"class": "stockValue"}).text for x in
                   soup_mysite.find_all("div", {"class": "nb_ann_cat clear"})]
    # print(Volume_adds)
    list_URL.extend(ids)
    list_VolAdds.extend(Volume_adds)
df_URL_Aimporter = pd.DataFrame({"ids": list_URL})
df_URL_Aimporter.ids.drop_duplicates()
df_VolAdd = pd.DataFrame({"VolAdds": list_VolAdds}, index=list_URL)
# print(df_URL_Aimporter)

if not os.path.exists(FileOut):
    print("Premier import")
    DF_URLS_merge = df_URL_Aimporter
else:
    print("Déjà eu un import ")
    BASE_dejaimporte = pd.read_csv(FileOut, sep=';')
    print("==> Nombre d'import :", len(BASE_dejaimporte))
    LIST_URL_dejaimporte = BASE_dejaimporte["index"]
    df_URL_dejaimporte = pd.DataFrame({"ids": LIST_URL_dejaimporte})
    df_URL_dejaimporte.drop_duplicates()
    print(df_URL_dejaimporte)
    DF_URLS_merge = pd.merge(df_URL_Aimporter, df_URL_dejaimporte, on="ids", how="left", indicator=True)
    DF_URLS_merge = DF_URLS_merge.loc[DF_URLS_merge._merge == "left_only"]
    print(DF_URLS_merge)

dict_infos = {}
LIST_URLS = DF_URLS_merge.ids.tolist()
for i, ID in enumerate(LIST_URLS):
    # print(i,"URL :",LIST_URLS[i])
    if i % 3 == 0:
        time.sleep(randint(1, 2))
    url_website = LIST_URLS[i]
    print(i, " ", url_website)
    # Création d'un dictionaire Python avec pour clef principal l'ID de la voiture
    dict_infos[url_website] = {}
    # print(df_VolAdd["VolAdds"].loc[url_website])
    dict_infos[url_website]["Volume_adds"] = df_VolAdd["VolAdds"].loc[url_website]
    try:
        soup_mysite = scrAPI.DOM_extract(user, password, url_website, chrome=False, sleep=False)
        # print(soup_mysite.find_all('div', {"class":"pW10"}))
        dict_infos[url_website]["Name"] = soup_mysite.find('div', {"class": "pW10"}).find('h2', {
            "class": "societyName uppercase bold"}).text
        try:
            dict_infos[url_website]["CPOSTAL"] = \
            soup_mysite.find('div', {"class": "pW10"}).findAll('span', {"class": "societyAddress"})[0].text
        except:
            dict_infos[url_website]["CPOSTAL"] = None
        try:
            dict_infos[url_website]["SIREN"] = \
            soup_mysite.find('div', {"class": "pW10"}).findAll('span', {"class": "societySiren"})[0].text.replace(
                "SIREN ", "")
        except:
            dict_infos[url_website]["SIREN"] = None
        try:
            dict_infos[url_website]["SIRET"] = \
            soup_mysite.find('div', {"class": "pW10"}).findAll('span', {"class": "societySiren"})[1].text.replace(
                "SIRET ", "")
        except:
            dict_infos[url_website]["SIRET"] = None
    except:
        dict_infos[url_website]["Name"] = None
        dict_infos[url_website]["CPOSTAL"] = None
        dict_infos[url_website]["SIREN"] = None
        dict_infos[url_website]["SIRET"] = None

print(dict_infos)

df = pd.DataFrame(dict_infos).transpose()
df = df.reset_index()

if not os.path.exists(FileOut):
    try:
        df.to_csv(FileOut, index=False, sep=";", encoding="ISO-8859-1")
    except:
        df.to_csv(FileOut, index=False, sep=";")
else:
    with open(FileOut, 'a') as f:
        try:
            df.to_csv(f, index=False, sep=";", encoding="ISO-8859-1", header=None)
        except:
            df.to_csv(f, index=False, sep=";", header=None)