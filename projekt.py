import pickle
import requests
from os import path, environ
from datetime import date, time, datetime 

URL = 'https://docs.google.com/forms/d/e/1FAIpQLScZS4UrEoWnGTwJRk1tlnFBYC_5NseUuGw_M0b9_dEJVlcD4Q/formResponse'
forms_seaded= {   
    'matrikel':'entry.1781272417',
    'nimi':'entry.1563459466',
    'ruum':'entry.1822655900',
    'aasta':'entry.369770644_year',
    'kuu':'entry.369770644_month',
    'päev':'entry.369770644_day',
    'kellaaeg':'entry.1339978028'
}

def kuupäev():   
    aeg = datetime.now().date()
    return aeg.strftime('%d %m %Y').split()  # salvestan kuupäeva listi formaadis [päev, kuu, aasta]


def kellaaeg():     # võtab praeguse kellaaja ja tagastab selle õiges vahemikus formi jaoks
    aeg = datetime.now().time()

    if aeg < time(10,00):
        return kellaaeg_sõne(time(8,0), time(10,00))
    elif aeg < time(12,00):
        return kellaaeg_sõne(time(10,00),time(12,00))
    elif aeg < time(16,00):
        return kellaaeg_sõne(time(14,00), time(16,00))
    elif aeg < time(18,00):
        return kellaaeg_sõne(time(16,00), time(18,00))
    elif aeg < time(23,59):
        return kellaaeg_sõne(time(18,00),time(20,00))   

def kellaaeg_sõne(aeg1, aeg2):
    aeg1 = aeg1.strftime('%H:%M')
    aeg2 = aeg2.strftime('%H:%M')

    return f'{aeg1}-{aeg2}'

def esimene_käivitus():       
    ### esmakordsel käivitamisel küsitakse nimi ja matrikli/number või isikukood

    nimi = input('Sisesta ees-ja perekonnanimi: ')
    matrikel = input('Sisesta matrikli number või isikukood: ')

    ### salvestab andmed objekti ja siis faili

    andmed = {
        'matrikel': matrikel,
        'nimi': nimi
    }       

    with open('save.p', 'wb') as faili:
        pickle.dump(andmed, faili)

def andmete_saatmine(andmed, seaded):
    saatmiseks = {}
    for key, value in seaded.items():
        saatmiseks[value] = andmed[key]
    return saatmiseks


##################################################
####  PÕHIPROGRAMM  ##############################
##################################################

print('\nTegemist on skriptiga, mis sisestab andmeid registreerimislehele')
print('Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.')


if not (path.exists('save.p')):     # Kui käivitakse esimest korda, küsitakse nime ja matrikli numbrit
    esimene_käivitus()

andmed_failist = {}

with open('save.p', 'rb') as failist:
    andmed_failist = pickle.load(failist)
#print(andmed_failist)

kuupäev = kuupäev()
kellaaeg = kellaaeg()

print(f'\nNimi: {andmed_failist["nimi"]}  matrikli nr/isikukood: {andmed_failist["matrikel"]} kellaaeg: {kellaaeg}  kuupäev: {kuupäev[0]}-{kuupäev[1]}-{kuupäev[2]}\n')

ruum = input('Sisesta ruumi number:  ')   

andmed_failist['ruum']= ruum
andmed_failist['aasta'] = kuupäev[2]
andmed_failist['kuu'] = kuupäev[1]
andmed_failist['päev'] = kuupäev[0]
andmed_failist['kellaaeg'] = kellaaeg

with open('save.p', 'wb') as faili:    #salvestan kogu info save.p faili
    pickle.dump(andmed_failist, faili)


andmed = pickle.load(open('save.p', 'rb'))
vastus = andmete_saatmine(andmed, forms_seaded)
r = requests.post(URL,data=vastus)


if r.status_code == 200:
     print("\nAndmed edukalt saadetud. ")
else:
    print("Andmete saatmisel tuli viga, proovige uuesti.")
    

while True:
    userinp = input("Kui soovite, võite ka tänase päeva kõikide toimuvate tunnide eest juba ära täita, \nKirjutage 'JAH' või kui ei soovi, siis sulge terminal või sisestage tühik: ")
    if userinp.upper() == "JAH":
        kellinput = input("Sisestage kellaaeg oma soovitud tunniks kujul xx:xx-yy:yy ")
        ruuminput = input("Sisestage ruum oma soovitud tunniks: ")
        andmed["kellaaeg"] = kellinput
        andmed["ruum"] = ruuminput
        #print(andmed)
        uusand = andmete_saatmine(andmed, forms_seaded)
        uusreq = requests.post(URL,data=uusand)
        if uusreq.status_code == 200:
            print("\nAndmed edukalt saadetud. ")
        else:
            print("Andmete saatmisel tuli viga, proovige uuesti.")
    else:
        break

