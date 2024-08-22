#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 20:50:38 2021

@author: priwi
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


MENO = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HESLO = "xxxxxxxxxxxxxxxxxxxxxxxxx"
#   Urcenie prehliadaca selenium 
driver = webdriver.Chrome('')

#   Otvorenie webowej stranky
driver.get("http://supplier.uber.com/orgs/4b93d203-ed0f-4e12-99ef-3f9411113574/reports")

#   vytlacenie/zobrazenie titulu stranky
print(driver.title)

#   Definovanie pola pre prihlasovacie meno a heslo 
prihlasenie_email = driver.find_element("id", "PHONE_NUMBER_or_EMAIL_ADDRESS" )

#   Definovanie prihlasovacieho mena
prihlasenie_email.send_keys(MENO)
prihlasenie_email.send_keys(Keys.RETURN)

time.sleep (15)
#sms detekcia

try:
    prihlasnie_SMS = driver.find_element("id", "alt-PASSWORD")
    print("Detekovanie hesla")
    time.sleep (30)
except NoSuchElementException:
    print("Element nenalezen")
    time.sleep(10)
    driver.close()
#   kliknutie na prihlasenie sa pomocou hesla
#prihlasenie_sheslo = driver.find_element("id", ("alt-PASSWORD"))
#prihlasenie_sheslo.click()
                            
time.sleep (3)


prihlasenie_heslo = driver.find_element("id", "PASSWORD" )
prihlasenie_heslo.send_keys(HESLO)
prihlasenie_heslo.send_keys(Keys.RETURN)

time.sleep (10)
#######################################################################

#klik na ponuku 
#ponukovy_strom = driver.find_element("class", "_css-hQrlmS")
#ponukovy_strom.click()

#klikni na kvalitu sofera
#kvalita_sofera = driver.find_element("class", "_css-dEMIui")
#kvalita_sofera.click()

#time.sleep (30)
#driver.close()

#   kliknutie na prihlasenie sa pomocou hesla
#prihlasenie_sheslo = driver.find_element("id", ("alt-PASSWORD"))
#prihlasenie_sheslo.click()
                            
#time.sleep (3)

# Definovanie pola na heslo 
#heslo = driver.find_element("id", "PASSWORD")
#   Definovanie hesla
#HESLO ="Priwitzer2345"

#heslo.send_keys(HESLO)
#heslo.send_keys(Keys.RETURN)

#prihlasenie_heslo.send_keys("Hchbqz4544!")




#driver.get("https://premium-limo-service.com/user/erste-hilfe/2")

#vignete = driver.find_element("class", "w-full m-0 text-xl font-semibold text-primary")

#vignete.click()


