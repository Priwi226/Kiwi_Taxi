#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 07:38:28 2023

@author: priwi
"""




nastup = 4 
cena_km = 1.18
cena_cas = 0.30 


Prehliadac_on = 0 # 1 spusteny prehliadac 
#Google_on_api = 1 if dnes % 2 == 0 else 0 #kazdy parny den
Google_on_api = 1 #### 1 zapnut
schedule_time_on = 0
Zvyhodneny_sofer_on = 1 # 1 = zapnute
Vyluceny_sofer_casovka_on = 1 # 1 = zapnute 

KNIHA_JAZD = 1  # 0 vypnute

Oktoberfest = 1

###         Podmienky
Min_cena = 0
Max_cena = 100000 
Min_km = 0
Max_km = 100

###################################### 
A = Alianz = [80939, 89451, 23665, ]
M = Messe =  [81829, 81823, 85609]
L = Lilienalle = [80939]
O = Olympia = ["Spiridon-Louis-Ring", "BMW", "Lerchenauer"]
OO = Oktoberfest = [81373, 80339, 80336, 80337, 80335, "Hans-Fischer-Stra"
                    , "Theresienwiese", "Gotheplatz", "Oktoberfest", "Wiesn"]
PSC_vyzdvyhnutia = (O, A, L)
PSC_cielu = (O, A, L)



######################################################
Vyluceny_sofer = ["Pet", "Jozko"]

Zvyhodneny_sofer = {
    "Per": 60,
    "Nikol": 1,
    "Fare": 1,
    }


###         Stroj
STROJ = ("Master")

###         Prihlasovanie na stranku
MENO = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
HESLO = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

Odmlka = int(5)

###         Telegram Data
Telegram_api_Token_uber = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
Telegram_api_Token_kiwi = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
Telegram_miestnost_kiwi = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")  #---- KIWI
Telegram_miestnost_uber = ("xxxxxxxxxxxxxxx")  #---- Auftrags
Telegram_miestnost_ja = ("xxxxxxxxxxxxxxxxx")  #---- Uber zakazky
URL = ("f'https://api.telegram.org/bot{apiToken}/sendMessage'")
Telegram_mazanie = "300"


###         SMS data
Sms_kluc = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

##FTP Nadstavenia 
Download_add = ("/home/priwi/Stiahnuté")

FTP_NAME = ("xxxxxxxxxxxxxxxxx")
FTP_MENO = ("xxxxxxxxxxxxxxxxx")
FTP_HESLO = ("xxxxxxxxxxxxxxxxx")
FTP_Cesta = ("/Python")
FTP_SUBOR = ("Uber_clicker.txt")
FTP_cas = 63

Nazov_subory =("driver_performance.csv")

####        Definovanie slov
Povodny_nazov_obsahuje = ("Driver Quality")
slovo = ("Kvalita vodiča")



###### Email nadstavenia
SMTP = ("smtpxxxxxxxxxxxxxxxxxxxxxx")
IMAP = ("imapxxxxxxxxxxxxxxxxxxxxxx")
Email_meno = ("xxxxxxxxxxxxxxxxxxxxxxx")
Email_heslo = ("xxxxxxxxxxxxxxxxxxx")
Odosielatel = ("xxxxxxxxxxxxxxxxxxxxx")
Predmet = ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


####   Google API
Googleapi =  ("xxxxxxxxxxxxxxxxxxxxxxxxxx")

Casovy_rozvrh = {
    "monday": {
        '04:00-05:00': 19,
        '05:00-07:00': 17,
        '07:00-08:00': 15,
        '08:00-09:00': 18,
        '09:00-12:00': 10,
        '12:00-19:00': 10,
        '19:00-20:00': 13
    },
    "tuesday": {
        '04:00-08:00': 12,
        '08:00-11:00': 12,
        '11:00-16:00': 10,
        '16:00-17:00': 12,
        '17:00-19:00': 10,
        '19:00-20:00': 10,
    },
    "wednesday": {
        '04:00-05:00': 19,
        '05:00-06:00': 17,
        '06:00-07:00': 19,
        '07:00-08:00': 19,
        '08:00-12:00': 10,
        '12:00-13:00': 10,
        '13:00-15:00': 10,
        '15:00-18:00': 11,
        '18:00-19:00': 10,
        '19:00-20:00': 10
    },
    "thursday": {
        '06:00-07:00': 15,
        '07:00-11:00': 13,
        '11:00-12:00': 18,
        '12:00-16:00': 11,
        '16:00-17:00': 13,
        '17:00-18:00': 10,
        '18:00-19:00': 10,
        '19:00-20:00': 10
    },
    "friday": {

        '00:00-05:00': 10,
        '05:00-06:00': 14,
        '06:00-07:00': 14,
        '07:00-08:00': 18,
        '08:00-11:00': 12,
        '11:00-12:00': 10,
        '13:00-19:00': 13,
        '19:00-23:00': 10,
        '23:00-23:59': 10
    },
    "saturday": {
        '00:00-01:00': 11,
        '01:00-02:00': 15,
        '02:00-03:00': 15,
        '03:00-04:00': 17,
        '04:00-05:00': 15,
        '05:00-07:00': 15,
        '07:00-09:00': 15,
        '09:00-18:00': 15,
        '18:00-19:00': 15,
        '19:00-20:00': 15,
        '20:00-22:00': 16,
        '22:00-23:59': 15,
    },
    "sunday": {
        '00:00-04:00': 15,
        '04:00-05:00': 15,
        '05:00-09:00': 15,
        '09:00-10:00': 15,
        '10:00-11:00': 15,
        '11:00-17:00': 15,
        '17:00-18:00': 11,
        '18:00-19:00': 11,
        '19:00-20:00': 11,
    }
}



test = 0


