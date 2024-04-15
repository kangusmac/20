import pandas as pd
# from pathlib import Path
# from enum import Enum
import re
import logging

#from frekvens import næste_tømningsdag, find_frekvens
from menupunkt import menupunkt_indeks, menupunkter, oversæt

#logger = logging.getLogger('lillebil')
logger = logging.getLogger(__name__)
                
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# File_handler = logging.FileHandler('lillebil.log')
# File_handler.setFormatter(formatter)

# logger.addHandler(File_handler)



LILLEBIL_DATA = pd.read_csv('lillebil_data.csv')
LILLEBIL_DATA['postnr'] = LILLEBIL_DATA['postnr'].astype(str)
# Skal ændres til FREKVENS
# Fordi ml, mu, tu, tl angiver hvilken dag og uge tømningen foregår, altså frekvensen
GRUPPE = ''


# menupunkter= ['Mandag - Lige', 'Mandag - Ulige', 'Torsdag - Lige', 'Torsdag - Ulige']
# # oversæt menupunkter til kolonnenavne
# oversæt = {'Mandag - Lige': 'ml', 'Mandag - Ulige': 'mu', 'Torsdag - Ulige': 'tu', 'Torsdag - Lige': 'tl'}




def hent_tømninger(dag_uge: str)-> pd.DataFrame:
    global GRUPPE
    GRUPPE = dag_uge
    logger.info(f'Der blev søgt på Gruppe: {dag_uge}')


    GRUPPE = oversæt[dag_uge]

    # dag_og_uge = oversæt[dag_uge]
    # df = LILLEBIL_DATA[LILLEBIL_DATA[dag_og_uge]]
    # return df



# søg på adresse
def find_adresse(adresse: str)-> pd.DataFrame:
    adresse = adresse
    adresse_fundet = []
    adresse_regex = re.compile(rf'{adresse}', re.IGNORECASE)
    for row in LILLEBIL_DATA.itertuples():
        if adresse_regex.findall(row.adresse):
            adresse_fundet.append(row)

    if adresse_fundet:
        adresse_fundet = pd.DataFrame(adresse_fundet)
        adresse_fundet.drop_duplicates(subset=['adresse'], inplace=True)
        return adresse_fundet
    else:
       # return 'Ingen adresse fundet'
        raise ValueError(f'Ingen adresse fundet: {adresse}')



# Midlertidig løsning
#def volumen(dag_uge, kolonnenavn):
def volumen(kolonnenavn):
    #df = hent_tømninger(dag_uge)
    df = LILLEBIL_DATA[LILLEBIL_DATA[GRUPPE]]
    #pd.DataFrame(df['type'].value_counts())
    #rename index to volumen
    df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')#.to_csv('volumen.csv', index=False)
    #df['type'].value_counts().reset_index(name='antal')
    #return df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')
    return df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')

# def angiv_antal(kolonnenavn):
#     df = udsnit()
#     #pd.DataFrame(df['type'].value_counts())
#     #rename index to volumen
#     df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')#.to_csv('volumen.csv', index=False)
#     #df['type'].value_counts().reset_index(name='antal')
#     return df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')

def hent_info(betingelse = None, info = None, sum = False):

    # Betingelse : bool

    # info : str
    #
    
    # hent_tømninger = oversæt[session_state[menu_key]]
    # df = LILLEBIL_DATA[LILLEBIL_DATA[hent_tømninger]]

    #df = hent_tømninger(GRUPPE)

    df = LILLEBIL_DATA[LILLEBIL_DATA[GRUPPE]]
    
    # default kolonner
    kolonner = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr']
  
    if info is not None:
        kolonner.append(info)

    # if column2 == '':
    #     columns = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr']
    # else:
    #     if column2 in df.columns:
    #        columns = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'] + [column2]
    #     else:
    #         raise AttributeError(f'{column2} not in columns')
    
    if  betingelse is None:
        #df = df.groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
        df = df.groupby(kolonner)['antal'].sum(numeric_only=True)
    else:
        #df = df[df[column]].groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
        df = df[df[betingelse]].groupby(kolonner)['antal'].sum(numeric_only=True)

    if sum:
        return df.sum()
    
    df = df.reset_index()
    df.sort_values(by=['vejnavn', 'husnr'], ascending=True, inplace=True)
    df.drop(columns=['vejnavn', 'husnr'], inplace=True)
    return df


# lav en funktion der tillader flere arg






# Bliver ikke brugt - bibeholdes indtil videre, som forlæg.
def angiv_betingelse(betingelse = None, info = None):

    # Betingelse : bool

    # info : str
    
    
    # udsnit = oversæt[session_state[menu_key]]
    # df = LILLEBIL_DATA[LILLEBIL_DATA[udsnit]]

    df = udsnit()
    
    # default kolonner
    kolonner = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr']
  
    if info is not None:
        kolonner.append(info)

    # if column2 == '':
    #     columns = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr']
    # else:
    #     if column2 in df.columns:
    #        columns = ['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'] + [column2]
    #     else:
    #         raise AttributeError(f'{column2} not in columns')
    
    if  betingelse is None:
        #df = df.groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
        df = df.groupby(kolonner)['antal'].sum(numeric_only=True)
    else:
        #df = df[df[column]].groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
        df = df[df[betingelse]].groupby(kolonner)['antal'].sum(numeric_only=True)
    
    df = df.reset_index()
    df.sort_values(by=['vejnavn', 'husnr'], ascending=True, inplace=True)
    df.drop(columns=['vejnavn', 'husnr'], inplace=True)
    return df


# gruppenavn
def angiv_navn_på_gruppe(gruppe : str)-> str:
    return gruppe






if __name__ == "__main__":
    pass