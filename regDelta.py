#!python3
import pickle
import requests
from os import path
from datetime import date, time, datetime
import pprint

import click

URL = 'https://docs.google.com/forms/d/e/1FAIpQLScZS4UrEoWnGTwJRk1tlnFBYC_5NseUuGw_M0b9_dEJVlcD4Q/formResponse'
#URL = 'https://docs.google.com/forms/d/e/1FAIpQLScZS4UrEoWnGTwJRk1tlnFBYC_NseUuGw_M0b9_dEJVlcD4Q/formResponse'

forms_seaded = {
    'matrikel': 'entry.1781272417',
    'nimi': 'entry.1563459466',
    'ruum': 'entry.1822655900',
    'aasta': 'entry.369770644_year',
    'kuu': 'entry.369770644_month',
    'päev': 'entry.369770644_day',
    'kellaaeg': 'entry.1339978028'
}


def päev():
    aeg = datetime.now().date()
    return aeg.strftime('%d %m %Y').split()
#           salvestan kuupäeva listi formaadis [päev, kuu, aasta]


def aeg(aeg=datetime.now().time()):

    #           võtab praeguse kellaaja ja tagastab selle õiges vahemikus formi jaoks

    if aeg < time(10, 00):
        return kellaaeg_sõne(time(8, 0), time(10, 00))
    elif aeg < time(12, 00):
        return kellaaeg_sõne(time(10, 00), time(12, 00))
    elif aeg < time(16, 00):
        return kellaaeg_sõne(time(14, 00), time(16, 00))
    elif aeg < time(18, 00):
        return kellaaeg_sõne(time(16, 00), time(18, 00))
    elif aeg < time(23, 59):
        return kellaaeg_sõne(time(18, 00), time(22, 00))


def kellaaeg_sõne(aeg1, aeg2):
    aeg1 = aeg1.strftime('%H:%M')
    aeg2 = aeg2.strftime('%H:%M')

    return f'{aeg1}-{aeg2}'


def esimene_käivitus():

    # esmakordsel käivitamisel küsitakse nimi ja matrikli/number või isikukood

    print('''
See Püütoni skript, aitab lihtsamini sisestada andmeid Delta registreerimislehele.\n
Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.

Skript salvestab nime ja matrikli koodi. Skripti käivitamisel on vaja lisada ainult ruuminumber.     
        ''')

    nimi = click.prompt('Sisesta ees-ja perekonnanimi', type=str)
    matrikel = click.prompt('Sisesta matrikli number või isikukood', type=str)


# salvestab andmed objekti ja siis faili

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

    try:
        tulemus = requests.post(URL, data=saatmiseks)
        tulemus.raise_for_status()
        print("\nAndmed edukalt saadetud. ")
        save_logi(andmed, "Saadetud")

    except requests.exceptions.HTTPError as err:

        print("Andmete saatmisel tuli viga, palun proovige uuesti.")
        save_logi(andmed, "Tõrge saatmisel")
        raise SystemExit(err)

    return tulemus


def kuva_andmed(andmed):
    click.confirm(f'''

Nimi: {andmed["nimi"]}
matrikli nr/isikukood: {andmed["matrikel"]}
kellaaeg: {andmed["kellaaeg"]}  
kuupäev: {andmed['päev']}-{andmed['kuu']}-{andmed['aasta']}
ruum: {andmed['ruum']}


Kas saadan andmed ära?
    ''', abort=True)


def save_logi(andmed, olek):
    logi = []
    andmed['Status'] = olek

    if (path.exists('logi.p')):
        logi = pickle.load(open('logi.p', 'rb'))
        logi.append(andmed)
    else:
        logi.append(andmed)

    pickle.dump(logi, open('logi.p', 'wb'))

#           mooduli Click seadistus


@click.command()
@click.argument('ruum', type=str, required=False)
@click.option(
    '-c', '--config', default=False, is_flag=True,
    help='Kui soovid muuta nime ja koodi'
)
@click.option('-m', '--mitu', default=False, is_flag=True,
              help='Saab lisada kõiki tänase päeval toimunud tunde.\nProgramm küsib kellaaega ning ruuminumbrit.'
              )
@click.option('-l', '--logi', default=False, is_flag=True, help='Kuvab kõik saadetud andmed. ')
##################################################
####  PÕHIPROGRAMM  ##############################
##################################################
def main(ruum, config, mitu, logi):
    '''
    See Püütoni skript, aitab lihtsamini sisestada andmeid Delta registreerimislehele.\n
    Kuupäeva ja kellaaja tuletab programm ajast, mil programm käivitati.

    Skript salvestab nime ja matrikli koodi. Skripti käivitamisel on vaja lisada ainult ruuminumber. 
    '''

    if logi:
        logi_sisu = pickle.load(open('logi.p', 'rb'))
        pprint.pprint(logi_sisu)
        click.Context.exit(1)

    if not (path.exists('save.p')) or config:
        #       Kui käivitatakse skripti esimest korda või kasutaja seda soovib
        esimene_käivitus()

    andmed_failist = pickle.load(open('save.p', 'rb'))

#       Kellaaja ja kuupäeva genereerimine kui käivitatakse esimest korda

    kuupäev = päev()
    kellaaeg = aeg()

    andmed_failist['aasta'] = kuupäev[2]
    andmed_failist['kuu'] = kuupäev[1]
    andmed_failist['päev'] = kuupäev[0]
    andmed_failist['kellaaeg'] = kellaaeg

#       Saabi lisada mitut tundi korraga

    if mitu:
        while True:
            userinp = click.confirm(
                'Kui soovite, võite ka tänase päeva kõikide toimuvate tunnide eest juba ära täita, \nKirjutage \'y\' või kui ei soovi, siis kirjutage \'N\' või sisestage tühik: ', abort=True)
            if userinp:
                kellinput = click.prompt(
                    '''Sisestage kellaaeg kellaeg, mis nendest vahemikus:
                            08:00-10:00   10:00-12:00
                            12:00-14:00   14:00-16:00
                            16:00-18:00   18:00-20:00
                            
                            Ning formaadis tund:minut =>  15:20
                     ''')
                kellinput = datetime.strptime(kellinput, '%H:%M').time()
                kellinput = aeg(kellinput)

                ruuminput = click.prompt(
                    'Sisestage ruum oma soovitud tunniks: ')
                andmed_failist["kellaaeg"] = kellinput
                andmed_failist["ruum"] = ruuminput

                kuva_andmed(andmed_failist)

                vastus = andmete_saatmine(andmed_failist, forms_seaded)

            else:
                break

    if not ruum or mitu:
        #       Kui ruumi koos skripti käivitamisega, ei sisestaud, küsitakse uuesti
        ruum = click.prompt('Sisesta ruumi number', type=str)

    andmed_failist['ruum'] = ruum

    kuva_andmed(andmed_failist)

    vastus = andmete_saatmine(andmed_failist, forms_seaded)


if __name__ == "__main__":
    main()
