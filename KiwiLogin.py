import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from spravy import kiwi_send_to_telegram
import Nadstavenia



MENO = "xxxxxxxxxxxxxxxxx"
HESLO = "xxxxxxxxxxxxxxxxxx"




def Kiwi_login(driver):
   
    print(driver.title)
    time.sleep (3)
    ################################################

    # definovanie policka meno
    prihlasovacie_pole_meno =driver.find_element("name", "signin[username]")

    #vloztenie textu do pola prihlasovacie meno 
    prihlasovacie_pole_meno.send_keys(MENO)

    #definovanie pola pre heslo
    prihlasovacie_pole_heslo = driver.find_element("name", "signin[password]")

    #vlozenie textu do pola heslo 
    prihlasovacie_pole_heslo.send_keys(HESLO)

    # definovanie pola automaticke prihlasenie
    automaticke_prihlasenie = driver.find_element("name", "signin[remember]")

    # Zaskrtnuti pola automaticke prihlasenie 
    automaticke_prihlasenie.click()

    time.sleep (2)

    #Enter
    prihlasovacie_pole_heslo.send_keys(Keys.RETURN)

    ##############################################################
    time.sleep(5)
    print("Prihlasenie OK KIWI")
    kiwi_send_to_telegram("Prihlasenie \n" + (Nadstavenia.STROJ) + " KIWI \nOK")
    #####################################################
