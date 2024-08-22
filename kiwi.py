#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 20:50:38 2021
"""

import traceback
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.options import Options
from KiwiLogin import Kiwi_login
from Telo import Telo
from spravy import kiwi_send_to_telegram
import requests
import Nadstavenia 
import platform
import os 

user_name = os.getlogin()

# Získaj informácie o operačnom systéme
system_info = platform.system()
version_info = platform.version()

# Vytlač informácie
print(f"Operačný systém: {system_info}")
print(f"Verzia: {version_info}")

if "Linux" in system_info:
    chrome_driver = f"/home/{user_name}/chromedriver"
if "Windows" in system_info:
    chrome_driver = "C:/Selenium/chromedriver.exe"

telegram_mess = "RUF GLEICH ZUM CHEF. Auftrags system ist runtergefalen !!!!!! KIWI" + Nadstavenia.STROJ

try:
    if Nadstavenia.Prehliadac_on == 1:
        driver = webdriver.Chrome(chrome_driver)
    elif Nadstavenia.Prehliadac_on != 1:
        options = Options()
        options.add_argument("--headless")  # Nastavenie pre bezhlavý režim
        driver = webdriver.Chrome(chrome_driver, options=options)

    # Otvorenie webstránky
    driver.get("https://kiwitaxi.com/agent.php/orders")

    Kiwi_login(driver)
    
    Posledna_zakazka = None
    Adresa_vyzdvyhnutia = None
    Adresa_vylozenia = None
    old_tab =[]
    
    Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab, system_info, user_name)

except Exception as e:
    # Ak nastane zlyhanie, zaznamenajte chybovú správu
    error_message = str(e)
    
    # Získanie posledných dvoch riadkov kódu
    code_lines = traceback.format_exc().strip().split('\n')
    last_two_lines = code_lines[-3:]
    code_snippet = "\n".join(last_two_lines)
    error_message_with_code = f"{code_snippet}\n\n{error_message}"
    driver.quit()
    
    # Odoslanie Telegram správy s chybovou hláškou a výpisom kódu
    kiwi_send_to_telegram(telegram_mess + "\n\n" + error_message_with_code)
    print(telegram_mess + "\n\n" + error_message_with_code)
    
    # Získanie informácií o problematickom prvku
    element_info = ""
    if isinstance(e, selenium.common.exceptions.StaleElementReferenceException):
        element = driver.find_element_by_id("id_prvku")  # Nahraďte "id_prvku" skutočným identifikátorom prvku
        element_info = f"Prvok: {element.tag_name} s id={element.get_attribute('id')} a class={element.get_attribute('class')}"
        print("Informácie o problematickom prvku:")
        print(element_info)

    # Zápis do súboru Log.txt
    log_message = f"{telegram_mess}\n\n{error_message_with_code}\n\n{element_info}"
    with open("Log.txt", "w") as file:
        file.write(log_message)
    driver.quit()

# Zápis do súboru Log.txt
with open("Log.txt", "w") as file:
    file.write(telegram_mess + "\n\n" + error_message_with_code + "\n")
