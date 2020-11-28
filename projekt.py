#!/usr/bin/env python3

import pickle
import json
import requests
from os import path, environ
from datetime import date, time, datetime 

import click

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


def päev():   
    aeg = datetime.now().date()
    return aeg.strftime('%d %m %Y').split()  
# salvestan kuupäeva listi formaadis [päev, kuu, aasta]


def aeg():     

# võtab praeguse kellaaja ja tagastab selle õiges vahemikus formi jaoks
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
        return kellaaeg_sõne(time(18,00),time(22,00))   

def kellaaeg_sõne(aeg1, aeg2):
    aeg1 = aeg1.strftime('%H:%M')
    aeg2 = aeg2.strftime('%H:%M')

    return f'{aeg1}-{aeg2}'
    
def esimene_käivitus():       

### esmakordsel käivitamisel küsitakse nimi ja matrikli/number või isikukood
       
    click.get_current_context()

    nimi = click.prompt('Sisesta ees-ja perekonnanimi', type=str)
    matrikel = click.prompt('Sisesta matrikli number või isikukood', type=str)


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
    print(saatmiseks)
    saatmiseks_json = json.dumps(saatmiseks)
    print(saatmiseks_json)
    tulemus = requests.post(URL, data=saatmiseks_json)
    

    return tulemus  


##################################################
####  PÕHIPROGRAMM  ##############################
##################################################

@click.command()
@click.help_option()

@click.argument('ruum', type=str, required=False)
@click.option(
    '-c', '--config', default=False, is_flag=True,
    help='Kui soovid andmeid muuta, siis lisa see käsule juurde käivitamisel '
    )

def main(ruum, config):
    '''
    See Püütoni skript, aitab lihtsamini sisestada andmeid Delta registreerimislehele.\n
    Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.

    Skript salvestab nime ja matrikli koodi. Skripti käivitamisel on vaja lisada ainult ruuminumber. 
     
    '''
    print('\nTegemist on skriptiga, mis sisestab andmeid registreerimislehele')
    print('Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.')
    print(config)

    if not (path.exists('save.p')) or config:     

# Kui käivitatakse skripti esimest korda või kasutaja seda soovib 
        esimene_käivitus()
     

    with open('save.p', 'rb') as failist:
        andmed_failist = pickle.load(failist)

# Kellaaja ja kuupäeva genereerimine kui käivitatakse esimest korda

    kuupäev = päev()
    kellaaeg = aeg()

    
    if not ruum:

# kui ruumi koos skripti käivitamisega, ei sisestaud, küsitakse uuesti
        ruum = click.prompt('Sisesta ruumi number', type=str)

    
       
    click.confirm(f'''

Nimi: {andmed_failist["nimi"]}
matrikli nr/isikukood: {andmed_failist["matrikel"]}
kellaaeg: {kellaaeg}  
kuupäev: {kuupäev[0]}-{kuupäev[1]}-{kuupäev[2]}
ruum: {ruum}


Kas saadan andmed ära?

    ''', abort=True)

    andmed_failist['ruum']= ruum
    andmed_failist['aasta'] = kuupäev[2]
    andmed_failist['kuu'] = kuupäev[1]
    andmed_failist['päev'] = kuupäev[0]
    andmed_failist['kellaaeg'] = kellaaeg

    with open('save.p', 'wb') as faili:    
#salvestan kogu info save.p faili
        pickle.dump(andmed_failist, faili)


    andmed = pickle.load(open('save.p', 'rb'))

#print('@@', andmete_saatmine(andmed, forms_seaded))
    
    vastus = andmete_saatmine(andmed_failist, forms_seaded)

    if vastus.status_code == 200:
        print("\nAndmed edukalt saadetud. ")
    else:
        print("Andmete saatmisel tuli viga, palunA proovige uuesti.")


if __name__ == "__main__":
    main()



