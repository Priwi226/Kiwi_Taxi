#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:09:51 2023
@author: priwi
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime
import time
import re
import requests
from spravy import kiwi_send_to_telegram
import zapis_citanie_api_databaza
import pocitanie_trasy
import Nadstavenia


def Telo(driver, Posledna_zakazka, Adresa_vyzdvyhnutia, Adresa_vylozenia, old_tab, system_info, user_name):

    old = set()
    data_list = []

    posledna_zakazka = None

    while True:
        try:
            table = driver.find_element(By.CLASS_NAME, 'table')
            rows = table.find_elements(By.TAG_NAME, 'tr')
            new_data_list = []

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) > 3 and cells[3].text == 'Offer new':
                    order = cells[2].text
                    if order not in old:
                        Datum_cas = cells[1].text
                        order = cells[2].text
                        state = cells[3].text
                        Adresa_vyzdvyhnutia = cells[4].text
                        Adresa_vylozenia = cells[5].text
                        passenger_nummer = cells[6].text
                        sluzba = cells[7].text
                        client_cash = cells[9].text
                        contractor = cells[10].text
                        my_profit = cells[11].text
                        if contractor == "-":
                            contractor = 0

                        neu_tab = (Datum_cas, order, state, Adresa_vyzdvyhnutia, Adresa_vylozenia, passenger_nummer, sluzba)
                        new_data_list.append(neu_tab)

                        if neu_tab in old:
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print("\nHľadám nové objednávky KIWI - ", current_time, "")
                            if posledna_zakazka is not None:
                                print(posledna_zakazka)

                            time.sleep(10)
                        else:
                            print("Zmena v tabuľke. Vykonávam príslušné akcie.")
                            driver.refresh()
                            time.sleep(10)
                            old.add(neu_tab)
                            
                            # Predefinovanie neznamych "koli naslednemu scriptu"  --- Lenivost neopustaj ma 
                            
                            Adresa_Vyzdvyhnutia = Adresa_vyzdvyhnutia
                            Adresa_Vylozenia = Adresa_vylozenia
                            
                                # Po najdeny 'Offer new' spusta dalej script 
                            if state == 'Offer new' :  # 'Scheduled'        'Offer new'
                                time.sleep(2)
                                
                                # Odstranenie vsetkich neziaducich znaby aby zostal iba cisti ciselny format pre cislo zakazky
                                order = re.sub(r"[^0-9]", "", order)
                                
                                    # Zistenie ci premmenna kontraktor je vecsia ako 0 ak ano nasledne odstrany vsetky znaky okrem ciselnych znakov 
                                        #Nasledna zmeny hodnoty na FLOAT
                                if contractor != 0 and contractor != "" and contractor != None:
                                    print("c1" + contractor)
                                    contractor = re.sub(r"[^\-0-9]", "", contractor)  # ponechanie iba čísiel a znaku mínus
                                    print("c2" + contractor)
                                    contractor = f"{contractor}"  # konverzia na string
                                    print("c3" + contractor)
                                    
                                    # Zistenie ci premmenna client_cash je vecsia ako 0 ak ano nasledne odstrany vsetky znaky okrem ciselnych znakov 
                                        #Nasledna zmeny hodnoty na FLOAT
                                if client_cash != None and client_cash != "":
                                    client_cash = re.sub(r"[^0-9]", "", client_cash)
                                    client_cash = float(client_cash)
                                    
                                    # Zistenie ci premmenna my_profit je vecsia ako 0 ak ano nasledne odstrany vsetky znaky okrem ciselnych znakov 
                                        #Nasledna zmeny hodnoty na FLOAT
                                if my_profit != None and my_profit != "":
                                    my_profit = re.sub(r"[^0-9]", "", my_profit)
                                    my_profit = float(my_profit)
    
    
                                    # Premena par radicnych vyratov na konkretne vyrazy 
                                if "Terminal" in Adresa_Vyzdvyhnutia:
                                    Adresa_Vyzdvyhnutia = "Nordallee 25, 85356 München-Flughafen"
                                if "Messe Ost" in Adresa_Vyzdvyhnutia:
                                    Adresa_Vyzdvyhnutia = "Am Messesee 2, 81829 München"
                                if "Oktoberfest" in Adresa_Vyzdvyhnutia:
                                    Adresa_Vyzdvyhnutia = "St.-Pauls-Platz 11, 80336 München"
                                if "Theresienwiese" in Adresa_Vyzdvyhnutia:
                                    Adresa_Vyzdvyhnutia = "St.-Pauls-Platz 11, 80336 München"
                                
                                        # Adresa Vylozenia 
                                if "Terminal" in Adresa_vylozenia:
                                    Adresa_vylozenia = "Nordallee 25, 85356 München-Flughafen"
                                if "Messe Ost" in Adresa_vylozenia:
                                    Adresa_Vyzdvyhnutia = "Am Messesee 2, 81829 München"
                                if "Oktoberfest" in Adresa_vylozenia:
                                    Adresa_vylozenia = "St.-Pauls-Platz 11, 80336 München"
                                if "Theresienwiese" in Adresa_vylozenia:
                                    Adresa_Vylozenia = "St.-Pauls-Platz 11, 80336 München"
                                    
                                    
                                #   Zistovanie konkretnych adries na zaklade google API 
                                    # Pouzitie pomocneho scriptu "zapis_citanie_api_databaza.najdi_adresu"
                                id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_Vyzdvyhnutia)
                                Adresa_Vyzdvyhnutia = total_address
                                start_link = link
                                # Kontrola priradenich neznamich 
                                    
                                if start_link == None:
                                    start_link = ("http://maps.google.com/maps?q=" + Adresa_Vyzdvyhnutia)
                                    
                                source_vyzdvyhnutie = source
                                
                                if source_vyzdvyhnutie == None:
                                    source_vyzdvyhnutie = ("vstup")
                                    
                                # Premenna premmennych na NONE
                                id_address = None
                                total_address = None
                                link = None
                                source = None
                                
                                    ##################################################
                                    
                                id_address, total_address, link, source = zapis_citanie_api_databaza.najdi_adresu(Adresa_vylozenia)
                                
                                ciel_link = link
                                
                                Adresa_Vylozenia = total_address
                                
                                if Adresa_Vylozenia == None:
                                    Adresa_Vylozenia = Adresa_vylozenia
                                    ciel_link = link
                                    
                                if ciel_link == None:
                                    ciel_link = ("http://maps.google.com/maps?q=" + Adresa_Vylozenia)
                                    
                                source_vylozenia = source
                                
                                if source_vylozenia == None:
                                    source_vylozenia = "vstup"
                                    
                                
                                total_address = None
                                link = None
                                source = None
                                
                                if source == None:
                                    source = "vstup"
                                ##################################################  Pocitanie trasy        
                                vzdialenost, cas, cesta_link, source = ( 
                                    pocitanie_trasy.spracovat_adresy(Adresa_Vyzdvyhnutia, Adresa_Vylozenia, 
                                    Nadstavenia.Google_on_api, Nadstavenia.Googleapi)
                                    )
                                
                                # Extrahujte hodiny a minúty pomocou regulárneho výrazu
                                try:
                                     vysledok = re.findall(r'\d+', cas)
                                     pocet_prvkov = len(vysledok)
                                 
                                     if pocet_prvkov == 1:
                                         minuty = int(vysledok[0])
                                         celkove_minuty = minuty
                                         
                                     else:
                                         hodiny = int(vysledok[0])
                                         minuty = int(vysledok[1])
                                         celkove_minuty = hodiny * 60 + minuty
                                 
                                     cas_cesty = celkove_minuty
                                                                  
                                except:
                                     cas_cesty = None
                                
                                # sources = source
                                
                                if vzdialenost == None:
                                    vzdialenost = "Km"
                                                    
                                if cesta_link == None:
                                    cesta_link = f"https://www.google.com/maps/dir/?api=1&origin={Adresa_Vyzdvyhnutia}&destination={Adresa_Vylozenia}&travelmode=car"
                                    
                                if client_cash > 0:
                                    print ("client cash: " + str (client_cash))
                                    print ("Contractor: " + str (contractor))
                                    Cena = float(client_cash) + float(contractor)
                                    print ("Cena: " + str(Cena))
                                    peniaze = "Cash"
                                    
                                if client_cash == None or client_cash == 0:
                                    Cena = my_profit
                                    peniaze = "Contractor"
                                    
                                vzdialenost = vzdialenost.replace("KM", "").replace ("Km", "").replace ("km", "").replace("m", "")
                                
                                if vzdialenost > str(0):
                                    vzdialenost = float (vzdialenost)
                                    cena_km_o = float(Cena)/float(vzdialenost)
                                    cena_km = round(cena_km_o, 2)
                                    vzdialenost = str(vzdialenost)
                                    cas_cesty = str(cas_cesty)
                                    
                                if vzdialenost == None or 0:
                                    vzdialenost = float(1)
                                    cena_km = float(1)
                                    
                                #   Potvrdenie ceny nizka / ok    
                                    
                                if 1.3 <= float(cena_km):
                                    if "Micro" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"    
                                
                                if 1.3 <= float(cena_km):
                                    if "Economy" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"
                                
                                if 1.3 <= float(cena_km):
                                    if "Comfort" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"
                                    
                                if 1.7 <= float(cena_km):
                                    if "Business" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"
                                    
                                if 1.7 <= float(cena_km):
                                    if "Minibus" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"
                                    
                                if 1.7 <= float(cena_km):
                                    if "Premium Minibus" in sluzba:
                                        cena_ok = "OK"
                                else:
                                    cena_ok = "NIZKA"
                                    cena_ok_r = float(cena_km) - 1.7
                                    cena_ok_r = round(cena_ok_r, 2)
                                    cena_ok_r = str(cena_ok_r)
                                    
                                    
                                # Vytvorenie tela Telegram spravy     
                                
                                if cena_ok == "OK":
                                    telegram_message = (
                                        "<b>" + str(Datum_cas) + "</b> \n" + sluzba + " / " +  str(passenger_nummer) + "\n" + "<b>" + peniaze + "\n"+ str(Cena) + 
                                        " €\nCena Km : " + str(cena_km) + " €\km" + " " + (cena_ok) + "\n<a href='" + cesta_link + "'>" + vzdialenost + " Km" + " / " + cas + "</a> </b>" + "\n" + "<a href='" + start_link + 
                                        "'>" + Adresa_Vyzdvyhnutia + "</a>\n ---------> \n" + "<a href='" + ciel_link + "'>" + Adresa_Vylozenia + 
                                        "</a>\n" + source + "\n" + "Order : " + order
                                        )
                                    
                                if cena_ok == "NIZKA":
                                    telegram_message = (
                                        "<b>" + str(Datum_cas) + "</b> \n" + sluzba + " / " +  str(passenger_nummer) + "\n" + "<b>" + peniaze + "\n"+ str(Cena) + 
                                        " €\nCena Km : " + str(cena_km) + " €\km" + " " + (cena_ok) + " "+ (cena_ok_r) + "\n<a href='" + cesta_link + "'>" + vzdialenost + " Km" + " / " + cas + "</a> </b>" + "\n" + "<a href='" + start_link + 
                                        "'>" + Adresa_Vyzdvyhnutia + "</a>\n ---------> \n" + "<a href='" + ciel_link + "'>" + Adresa_Vylozenia + 
                                        "</a>\n" + source + "\n" + "Order : " + order
                                        )
                                
                                # Odoslanie telegram spravy 
                                
                                kiwi_send_to_telegram(telegram_message)
                                
                                # Vytvorenie tela poslednej zakazky
                                
                                posledna_zakazka = (
                                    "Posledna zakazka:\n" + order + "\n    " + Datum_cas + "\n          " + 
                                    Adresa_Vyzdvyhnutia + "   -->   " + Adresa_vylozenia + ", " + sluzba + "\n" + str(Cena)
                                    )
                                
                                # Anulovanie vsetkych premennych na hodnotu None pre spravny chod programu 
                                
                                Datum_cas = None
                                order = None
                                state = None
                                Adresa_vyzdvyhnutia = None
                                Adresa_vylozenia = None
                                passenger_nummer = None
                                sluzba = None
                                client_cash = None
                                contractor = None
                                my_profit = None
                                Adresa_Vyzdvyhnutia = None
                                Adresa_Vylozenia = None
                                vzdialenost == None
                                client_cash == None
                                contractor == None
                                my_profit == None
                                continue
                                
                                
            
                            
            # Update data_list
            data_list = new_data_list

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("\nHľadám nové objednávky KIWI -", current_time, "")
            if posledna_zakazka is not None:
                print(posledna_zakazka)

            time.sleep(10)


        except StaleElementReferenceException:
            print("StaleElementReferenceException: Waiting for 5 seconds and then retrying...")
            driver.get("https://kiwitaxi.com/agent.php/orders")
            time.sleep(5)
            driver.refresh()
            time.sleep(30)
            continue  # Pokračovat od začátku smyčky