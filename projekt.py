import pickle

from os import path, environ
from datetime import date, time, datetime 

URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfw5ZCwsTYPg2pXUhkgXRDghVHLrVzbC1GRX4e7DDgs2q6NxQ/formResponse'
forms_seaded= {   
    'matrikel':'1002323025',
    'nimi':'5777754409',
    'ruum':'1770608055',
    'aasta':'1182929069_year',
    'kuu':'1182929069_month',
    'päev':'1182929069_paev',
    'kellaaeg':'2037560166'
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
    elif aeg < time(20,00):
        return kellaaeg_sõne(time(18,00),time(20,00))   

def kellaaeg_sõne(aeg1, aeg2):
    aeg1 = aeg1.strftime('%H:%M')
    aeg2 = aeg2.strftime('%H:%M')

    return f'{aeg1}-{aeg2}'
    
def esimene_käivitus():       
    ### esmakordsel käivitamisel küsitakse nimi ja martikli/number või isikukood

    nimi = input('Sisesta ees-ja perekonnanimi: ')
    martikel = input('Sisesta martikli number või isikukood: ')

    ### salvestab andmed objekti ja siis faili

    andmed = {
        'matrikel': martikel,
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
print('Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.\n')


if not (path.exists('save.p')):     # Kui käivitakse esimest korda, küsitakse nime ja martikli numbrit
    esimene_käivitus()

andmed_failist = {}

with open('save.p', 'rb') as failist:
    andmed_failist = pickle.load(failist)

print(f'\nNimi: {andmed_failist["nimi"]}  Martikli nr/isikukood: {andmed_failist["matrikel"]}\n')


ruum = input('Sisesta ruumi number:  ')    

kuupäev = kuupäev()
kellaaeg = kellaaeg()

andmed_failist['ruum']= ruum
andmed_failist['aasta'] = kuupäev[2]
andmed_failist['kuu'] = kuupäev[1]
andmed_failist['päev'] = kuupäev[0]
andmed_failist['kellaaeg'] = kellaaeg

with open('save.p', 'wb') as faili:    #salvestan kogu info save.p faili
    pickle.dump(andmed_failist, faili)

#################################### PRINT TESTID

andmed = pickle.load(open('save.p', 'rb'))

print('@@', andmete_saatmine(andmed, forms_seaded))
