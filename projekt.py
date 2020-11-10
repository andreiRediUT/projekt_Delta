import pickle
import os.path
from datetime import date, time, datetime 


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
    
def andmete_salvestus():       
    ### esmakordsel käivitamisel küsitakse nimi ja martikli/number või isikukood

    nimi = input('Sisesta ees-ja perekonnanimi: ')
    martikel = input('Sisesta martikli number või isikukood')

    ### salvestab andmed objekti ja siis faili

    andmed = {
        'martikel': martikel,
        'nimi': nimi
    }       

    with open('save.p', 'wb') as faili:
        pickle.dump(andmed, faili)


##################################################
####  PÕHIPROGRAMM  ##############################
##################################################


if os.path.exists('save.p'):    # kui kasutaja on varem nime ja koodi salvestanud, hakkab programm küsima ainult ruuminumbrit 
    andmed_failist = {}

    with open('save.p', 'rb') as failist:
        andmed_failist = pickle.load(failist)
    
    ruum = input('Nimi ning martikli nr on olemas.\n Sisesta ruumi number: ')    

    kuupäev = kuupäev()
    kellaaeg = kellaaeg()

    andmed_failist['päev'] = kuupäev[0]
    andmed_failist['kuu'] = kuupäev[1]
    andmed_failist['aasta'] = kuupäev[2]

    andmed_failist['kellaaeg'] = kellaaeg

    with open('save.p', 'wb') as faili:
        pickle.dump(andmed_failist, faili)
    
else: 
    andmete_salvestus()

#################################### PRINT TESTID


andmed = pickle.load(open('save.p', 'rb'))
print('@@', andmed)







    







