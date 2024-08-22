#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 22:35:33 2023
@author: priwi
"""

import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import re
import time
import requests
from datetime import datetime
from pywebcopy import save_webpage

def send_to_telegram(message):
    apiToken = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    chatID = "xxxxxxxxxxxxxxxxxxxxx"
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        formatted_message = """
        <b>Toto je tučný text</b>
        <i>Toto je text kurzívou</i>
        <code>Toto je blokový kód</code>
        <b><font color="red">Toto je červený text</font></b>
        <b><font color="green">Toto je zelený text</font></b>
        """
        
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message, 'parse_mode': 'HTML'})
        print(response.text)
    except Exception as e:
        print(e)

#################################  KIWI logIn ######################
###### Definovanie vyrazov
MENO = "XXXXXXXXX"
HESLO = "XXXXXXXXXXXXXXXX"

# Inicializácia prehliadača Chrome
driver = webdriver.Chrome('/home/zakazky/chromedriver') 

# Navigácia na stránku KIWI
driver.get("https://kiwitaxi.com/agent.php/orders")

# Vytvorenie zložky na uloženie obsahu
output_dir = "kiwi_zak"
os.makedirs(output_dir, exist_ok=True)

# Prihlásenie
prihlasovacie_pole_meno = driver.find_element("name", "signin[username]")
prihlasovacie_pole_meno.send_keys(MENO)

prihlasovacie_pole_heslo = driver.find_element("name", "signin[password]")
prihlasovacie_pole_heslo.send_keys(HESLO)

automaticke_prihlasenie = driver.find_element("name", "signin[remember]")
automaticke_prihlasenie.click()

prihlasovacie_pole_heslo.send_keys(Keys.RETURN)

# Počkajte na načítanie stránky
time.sleep(5)

old = set()
neu_tab = set()


while True:
    table = driver.find_element(By.CLASS_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        # if len(cells) > 3 and 'Scheduled' in cells[3].text:
        if len(cells) > 3 and cells[3].text not in ['Scheduled', 'Completed', 'Cancelled']:# Skontrolujte štvrtú bunku riadku
            order = cells[2].text
            neu_tab.add(order)

            if order not in old:
                date_start = cells[1].text
                order = cells[2].text
                state = cells[3].text
                from_location = cells[4].text
                to_location = cells[5].text
                passenger = cells[6].text
                additional_services = cells[7].text
                client_cash = cells[9].text
                contractor = cells[10].text
                my_profit = cells[11].text

                # Získanie zdrojového kódu stránky
                page_source = driver.page_source
                
                # Uloženie zdrojového kódu do HTML súboru
                with open(os.path.join(output_dir, "kiwi_page.html"), "w", encoding="utf-8") as f:
                    f.write(page_source)
                
                # Nastavenie Chrome pre stiahnutie pridružených zdrojov
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                
                # Vytvorenie novej inštancie prehliadača pre stiahnutie
                with webdriver.Chrome(chrome_options=chrome_options) as downloader:
                    downloader.get(driver.current_url)
                
                    # Počkajte na načítanie stránky
                    time.sleep(5)
                
                    # Stiahnutie a uloženie každého zdroja
                    for element in downloader.find_elements(By.TAG_NAME, "img"):
                        src = element.get_attribute("src")
                        if src:
                            response = requests.get(src, stream=True)
                            filename = os.path.join(output_dir, os.path.basename(src))
                            with open(filename, "wb") as img_file:
                                shutil.copyfileobj(response.raw, img_file)
                            del response
                            
                if state != ['Scheduled', 'Completed', 'Cancelled']:
                    order = re.sub(r"[^0-9]", "", order)
                    print(order)
                    link = driver.find_element(By.PARTIAL_LINK_TEXT, order)
                    link.click()
                    
                    
                    
                    output_dir = "kiwi_zak_ofer"
                    
                    # Získanie zdrojového kódu stránky
                    page_source = driver.page_source
                    
                    # Uloženie zdrojového kódu do HTML súboru
                    with open(os.path.join(output_dir, "kiwi_page.html"), "w", encoding="utf-8") as f:
                        f.write(page_source)
                    
                    # Nastavenie Chrome pre stiahnutie pridružených zdrojov
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")
                    
                    # Vytvorenie novej inštancie prehliadača pre stiahnutie
                    with webdriver.Chrome(chrome_options=chrome_options) as downloader:
                        downloader.get(driver.current_url)
                    
                        # Počkajte na načítanie stránky
                        time.sleep(5)
                    
                        # Stiahnutie a uloženie každého zdroja
                        for element in downloader.find_elements(By.TAG_NAME, "img"):
                            src = element.get_attribute("src")
                            if src:
                                response = requests.get(src, stream=True)
                                filename = os.path.join(output_dir, os.path.basename(src))
                                with open(filename, "wb") as img_file:
                                    shutil.copyfileobj(response.raw, img_file)
                                del response
                                
                    
                    
                    
                    
                    
                    
                    time.sleep(2)
                    xpath_expression = "//*[contains(text(), 'Distance')]"
                    element_distance = driver.find_element(By.XPATH, xpath_expression)
                    # Získame nadradený element (riadok)order = re.sub(r"[^0-9.,]", "", order)
                    row_element = element_distance.find_element(By.XPATH, "./ancestor::tr")
                    # Získame hodnoty všetkých stĺpcov v rámci tohto riadku
                    columns = row_element.find_elements(By.TAG_NAME,"td")
                    values = [column.text for column in columns]
                    closed = driver.find_element(By.CSS_SELECTOR,"a.close[href='#']")
                    closed.click()
                    time.sleep(1)
                    
                    if contractor !=0 and contractor != "":
                        contractor = re.sub(r"[^0-9]", "", contractor)
                        contractor = float(contractor)
                        
                    print("client cash")
                    print(client_cash)
                    
                    if client_cash != None and client_cash != "":
                        client_cash = re.sub(r"[^0-9]", "", client_cash)
                        client_cash = float(client_cash)
                        print("client cash zmena na float")
                        
                    if my_profit != None and my_profit != "":
                        my_profit = re.sub(r"[^0-9]", "", my_profit)
                        my_profit = float(my_profit)
                    
                    pos_km = values[1].find("km")

                    if pos_km != -1:
                        # Ak sa "km" nachádza v reťazci, pokračujeme s extrahovaním číselnej hodnoty pred "km"
                        vzdialenost = values[1][:pos_km].strip()
                        vzdialenost = float(vzdialenost)
                        print(vzdialenost)
                    else:
                        print("Text 'km' nebol nájdený v reťazci.")
                        vzdialenost = None
                        
                    print("vzdialenost")
                    print(vzdialenost)
                    print(type(vzdialenost))
                    print("Hodnoty riadku:", values[1])
                    print(type(values[1]))
                    print(order)
                    print('Dátum štartu:', date_start)
                    print('Objednávka:', order)
                    print('Stav:', state)
                    print('Z miesta:', from_location)
                    print('Do miesta:', to_location)
                    print('Cestujúci:', passenger)
                    print('Dodatočné služby:', additional_services)
                    print('Klient (hotovosť):', client_cash)
                    print('Dodávateľ:', contractor)
                    print('Môj zisk:', my_profit)
    
                    start_link = "http://maps.google.com/maps?q=" + from_location
                    ciel_link = "http://maps.google.com/maps?q=" + to_location

                    # telegram_message = (
                    #     "<b>" + date_start + "\n<a href='" + start_link + "'>" + from_location + "</a>\n ---------> \n" +
                    #     "<a href='" + ciel_link + "'>" + to_location + "</a>\n" + additional_services + "\n" +
                    #     "Cash:" + client_cash + "\nProfit:" + my_profit + "\nOrder:"  + 
                    #     order + "\nVzdialenost a cas: " + values[1] + "</b>"
                    # )
                    
                    print("client cash")
                    print(client_cash)
                    
                    
                    
                    
                    if client_cash > 0:
                        my_profit = (client_cash - contractor)
                        
                    cena_km_o = my_profit/vzdialenost
                    cena_km = round(cena_km_o, 2)
                        
                        
                    if client_cash > 0:
                        telegram_message = (
                            "<b>" + date_start + "\n<a href='" + start_link + "'>" + from_location + "</a>\n ---------> \n" +
                            "<a href='" + ciel_link + "'>" + to_location + "</a>\n" + additional_services + "\n" +
                            "CashProfit:  " + str(my_profit) + " €\nOrder:"  + order + "\nVzdialenost a cas: " + str(values[1]) + 
                             "\nCena na Km: " + str(cena_km) + " € </b>"
                            )
                    else:
                        telegram_message = (
                            "<b>" + date_start + "\n<a href='" + start_link + "'>" + from_location + "</a>\n ---------> \n" +
                            "<a href='" + ciel_link + "'>" + to_location + "</a>\n" + additional_services + "\n" +
                            "\nProfit:  " + str(my_profit) + " €\nOrder:"  + order + "\nVzdialenost a cas: " + str(values[1]) + 
                            "\nCena na Km: " + str(cena_km) + " € </b>" 
                            )
                        
    
                    send_to_telegram(telegram_message)
    
                    posledna_zakazka = (
                        "Posledna zakazka:\n" + order + "\n    " + date_start + "\n          " + \
                        from_location + "   -->   " + to_location + "\    " + additional_services
                        )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\nHľadám nové objednávky -", current_time, "")
    old = neu_tab.copy()
    
    time.sleep(10)



# ... (zvyšok vášho kódu)
