# %%
import datetime
import logging

logger = logging.getLogger('__name__')
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# File_handler = logging.FileHandler('menupunkt.log')
# File_handler.setFormatter(formatter)
# logger.addHandler(File_handler)
#logger.setLevel(logging.DEBUG)

## Statisk definerede variabler
#  Alias: SDM
# %%
# opret en liste med menupunkter
menupunkter= ['Mandag - Lige', 'Mandag - Ulige', 'Torsdag - Lige', 'Torsdag - Ulige']
# oversæt menupunkter til kolonnenavne
oversæt = {'Mandag - Lige': 'ml', 'Mandag - Ulige': 'mu', 'Torsdag - Ulige': 'tu', 'Torsdag - Lige': 'tl'}

# %%
oversæt_kode = { 0: 'Mandag - Lige', 1: 'Mandag - Ulige', 3: 'Torsdag - Lige', 4: 'Torsdag - Ulige'}
# oversæt kode til menupunkter

## Definerede funktioner
#  Alias: DF

# %%
def dags_dato() -> datetime.date:
    '''
    Funktionen returnerer dagens dato.
    '''

    return datetime.date.today()


# %%

def get_week_number(dato) -> int:
    '''
    Funktionen tager en dato som input og returnerer nummeret på ugen.
    '''
    #today = datetime.date.today()
    return dato.isocalendar()[1]


# %%
def ulige_eller_lige(uge:int) -> int:
    '''
    Funktionen tager et heltal som input (repræsenterende ugenummer)
    og returnerer 0 hvis ugen er lige og 1 hvis ugen er ulige.    

    '''
    if uge % 2 == 0:
        return 0
        return f"Lige uge {uge}"
    
    else:
        return 1
        return f"Ulige uge {uge}"


# %%
def get_weekday(dato):
    '''
    Funktionen tager en dato som input og returnerer nummeret på ugedagen.
    fra 0 til 6, hvor 0 er mandag og 6 er søndag.
    '''

    #today = datetime.date.today()
    return dato.weekday()



# %%
def mandag_eller_torsdag(dag):
    '''
    Funktionen tager et heltal som input (repræsenterende nummeret på ugedagen)
    og returnerer 0 hvis det er mandag og 3 hvis det er torsdag.
    '''

    if dag == 0:
        return 0
        return "Mandag"
    elif dag == 3:
        return 3
        return "Torsdag"
    else:
        return None
        return "Ikke mandag eller torsdag"
    

# %%
def get_next_weekday(weekday):
    today = datetime.date.today()
    days_ahead = weekday - today.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return today + datetime.timedelta(days_ahead)

# %%
def clousure(datoday):
    '''
    Funktionen tager en dato
    som input og returnerer en funktion, 
    der tager et heltal som input (repræsenterende nummeret på ugedagen) 
    og returnerer datoen for næste forekomst af ugedagen.
    '''
    def get_next_weekday(weekday):
        today = datoday
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return today + datetime.timedelta(days_ahead)
    return get_next_weekday

# %%
def næste_mandag_eller_torsdag_closure(dato):
    # Et eks
    get_next_weekday = clousure(dato)
    # Find the next monday or thursday using the function
    næste_dato= min([get_next_weekday(0), get_next_weekday(3)]) 
    næste_dag = næste_dato.weekday()
    næste_ugenummer = næste_dato.isocalendar()[1]
    # return tuple with the next day and the week number
    return næste_dag, næste_ugenummer, næste_dato


# %%
def næste_mandag_eller_torsdag():
    næste_dato= min([get_next_weekday(0), get_next_weekday(3)])
    næste_dag = næste_dato.weekday()
    næste_ugenummer = næste_dato.isocalendar()[1]
    # return tuple with the next day and the week number
    return næste_dag, næste_ugenummer, næste_dato

def test_dato(dato):
    logger.info(f'Der blev søgt på {dato}')
    dag = get_weekday(dato)
    uge = get_week_number(dato)
    Menupunkt = ''
    if  mandag_eller_torsdag(dag) == None:
        næste_dag, næste_ugenummer, dato = næste_mandag_eller_torsdag_closure(dato)
        #print("Næste dag er", næste_dag, "og det er", ulige_eller_lige(næste_ugenummer))
        kode = næste_dag + ulige_eller_lige(næste_ugenummer)
        #print("Koden er", kode)
        #print(oversæt_kode[kode])
        Menupunkt = oversæt_kode[kode]
    else:
        #print("Det er", mandag_eller_torsdag(dag), "og det er", ulige_eller_lige(uge))
        kode = dag + ulige_eller_lige(uge)
        #print("Koden er", kode)
        #print(oversæt_kode[kode])
        Menupunkt = oversæt_kode[kode]
    return Menupunkt


# # %%



# %%
## Dynamisk definerede globlale variabler
#  Alias: DDM

# Dato i dag
dato_i_dag = dags_dato()
dag_i_ugen = get_weekday(dato_i_dag)
nummeret_på_ugen = get_week_number(dato_i_dag)

tirsdag = datetime.date(2024, 3, 22)
menupunkt = test_dato(dato_i_dag)
menupunkt_indeks = menupunkter.index(menupunkt)



# %%
# dan forskellige datoer




if __name__ == '__main__':
    print(f'Dato i dag er {dato_i_dag}')
    print(f'Dag i ugen er {dag_i_ugen}')
    print(f'Nummeret på ugen er {nummeret_på_ugen}')
    # hvilket index har Menupunkt i menupunkter
    print(f'Menupunkt er {menupunkt}')
    print(f'Menupunkt er på index { menupunkter.index(menupunkt)}')
    

# %%
# test af funktionerne
# print(test_dato(dato_1))
# assert test_dato(dato_1) == 'Mandag - Lige'
# print(test_dato(dato_2))
# assert test_dato(dato_2) == 'Torsdag - Ulige'
# %%
# if mandag_eller_torsdag(dag_i_ugen) == None:
#     #print("Ikke mandag eller torsdag")
#     næste_dag, næste_ugenummer, dato = næste_mandag_eller_torsdag()
#     #print("Næste dag er", næste_dag, "og det er", ulige_eller_lige(næste_ugenummer))
#     kode = næste_dag + ulige_eller_lige(næste_ugenummer)
#     print("Koden er", kode)
#     print(oversæt_kode[kode])
#     Menupunkt = oversæt_kode[kode]
# else:
#     print("Det er", mandag_eller_torsdag(dag_i_ugen), "og det er", ulige_eller_lige(nummeret_på_ugen))
#     kode = dag_i_ugen + ulige_eller_lige(nummeret_på_ugen)
#     print("Koden er", kode)
#     print(oversæt_kode[kode])
#     Menupunkt = oversæt_kode[kode]

# %%
