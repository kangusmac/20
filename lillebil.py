import pandas as pd
import mymapslinks as mml
from pathlib import Path
from enum import Enum
import re
from frekvens import næste_tømningsdag, find_frekvens


LILLEBIL_DATA = pd.read_csv('lillebil_data.csv')
LILLEBIL_DATA['postnr'] = LILLEBIL_DATA['postnr'].astype(str)


menupunkter= ['Mandag - Lige', 'Mandag - Ulige', 'Torsdag - Lige', 'Torsdag - Ulige']
# oversæt menupunkter til kolonnenavne
oversæt = {'Mandag - Lige': 'ml', 'Mandag - Ulige': 'mu', 'Torsdag - Ulige': 'tu', 'Torsdag - Lige': 'tl'}

GRUPPE = ''


# --------------------------------------------- Config ---------------------------------------------




# søg på adresse
def find_adresse(adresse: str)-> pd.DataFrame:
    adresse = adresse
    adresse_fundet = []
    adresse_regex = re.compile(rf'{adresse}', re.IGNORECASE)
    for row in LILLEBIL_DATA.itertuples():
        if adresse_regex.findall(row.adresse):
            adresse_fundet.append(row)

    if adresse_fundet:
        return adresse_fundet
    else:
        return 'Ingen adresse fundet'

def vis_adresse(adresser: list) -> pd.DataFrame:
    resultat = adresser
    resultat = pd.DataFrame(resultat)
    resultat = resultat.drop_duplicates(subset=['adresse'])
    for row in resultat.itertuples():
        col1,col2 = st.columns([1,2])
        col1.write(row.adresse)
        col2.button('Vis detaljer', key= row.id, on_click= update_details, args=(row,))
        dag, dato = næste_tømningsdag(row.tur)
        #st.write(f'Tømmes {find_frekvens(row.tur)}')
        col1.write(f'Næste tømning: {dag} {dato}')
        st.markdown('---')




def vis_details():
    row = session_state[display_item]
    #row =pd.DataFrame(row)
    adresse = row.adresse
    #gade, postnr,by, land = row.adresse.split(',')
    st.subheader(adresse, anchor='details',divider=True)
    

    st.write(f'Følgende materiel er tilmeldt adressen:')
    resultat = session_state[search_result]
    resultat = pd.DataFrame(resultat)
    #resultat = resultat.groupby(['adresse', 'beholder'])['antal'].sum()
    resultat = resultat.groupby(['adresse', 'beholder']).size()


    col3, col4 = st.columns(2)
    with col3:
        st.markdown('Beholder:')
    with col4:
        st.markdown('Antal:')
    col1, col2 = st.columns(2)
    for beholder in resultat.loc[adresse].index:
         
         antal = resultat.loc[adresse][beholder]
         with col1:
            st.write(f'{beholder}')
         with col2:
            st.write(f'{antal:>}')
    st.write(f'Næste tømning: {næste_tømningsdag(row.tur)}')
    


def groupby2():
    udsnit = oversæt[session_state[menu_key]]
    df = LILLEBIL_DATA[LILLEBIL_DATA[udsnit]]
    #df['postnr'] = df['postnr'].astype(str)
    df = df.groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
    df = df.reset_index()
    df.sort_values(by=['vejnavn', 'husnr'], ascending=True, inplace=True)
    df.drop(columns=['vejnavn', 'husnr'], inplace=True)
    return df



def filtrere(betingelse = None, info = None):

    # Betingelse : bool

    # info : str
    #
    
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

def søg_på_betingelse(betingelse : str)-> pd.DataFrame:
    #df = LILLEBIL_DATA[LILLEBIL_DATA[betingelse]]
    df = udsnit(betingelse)
    return df

def søg_på_info(infovis : str)-> pd.DataFrame:
    df = filtrere(info=infovis)
    return df
# gruppenavn
def angiv_navn_på_gruppe(gruppe : str)-> str:
    return gruppe

# gruppedata
def søg_på_gruppe(gruppe : str)-> pd.DataFrame:
    df = LILLEBIL_DATA[LILLEBIL_DATA[gruppe]]
    return df

# ok
def udsnit(frekvens : str = None):
    udsnit = frekvens
    df = LILLEBIL_DATA[LILLEBIL_DATA[udsnit]]
    return df

# ok
def angiv_antal(kolonnenavn):
    df = udsnit()
    #pd.DataFrame(df['type'].value_counts())
    #rename index to volumen
    df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')#.to_csv('volumen.csv', index=False)
    #df['type'].value_counts().reset_index(name='antal')
    return df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')

class Gruppe:
    def __init__(self, gruppenavn):
        self.gruppenavn = gruppenavn
        self.df = LILLEBIL_DATA[LILLEBIL_DATA[self.gruppenavn]]

    def søg_på_betingelse(self, betingelse : str)-> pd.DataFrame:
        df = self.df[self.df[betingelse]]
        return df

    def søg_på_info(self, info : str)-> pd.DataFrame:
        df = self.df.groupby([info])['antal'].sum(numeric_only=True)
        df = df.reset_index()
        df.sort_values(by=[info], ascending=True, inplace=True)
        return df

    def angiv_navn_på_gruppe(self)-> str:
        return self.gruppenavn

    def gruppedata(self)-> pd.DataFrame:
        return self.df

    def angiv_antal(self, kolonnenavn):
        #pd.DataFrame(df['type'].value_counts())
        #rename index to volumen
        self.df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')#.to_csv('volumen.csv', index=False)
        #df['type'].value_counts().reset_index(name='antal')
        return self.df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')

    def udsnit(self, frekvens : str = None):
        udsnit = frekvens
        df = LILLEBIL_DATA[LILLEBIL_DATA[udsnit]]
        return df


    
def vis_data():
    st.write(f'## {session_state[menu_key]}')
    st.write('### Tømninger:')
    df = groupby()
    #st.table(df)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.checkbox('Debug', key='debug', value=False):
        st.data_editor(LILLEBIL_DATA)    


def vis_info():
    st.write(f'## {session_state[menu_key]}')
    st.write('### Info:')

    #udsnit = oversæt[session_state[menu_key]]
    #df = LILLEBIL_DATA[LILLEBIL_DATA[udsnit]]
    #df = groupby()
    #df['postnr'] = df['postnr'].astype(str) 

    # antal_alt= df['antal'].sum()
    # st.write(f'Antal tømninger: {antal_alt}')
    
    st.text('Fordelt på følgende størrelser(liter):')
    #antal_type = df.groupby(['type'])[["antal"]].sum(numeric_only=True).reset_index()
    antal_type = angiv_antal('type')
    st.dataframe(antal_type, use_container_width=True, hide_index=True)
 
    # antal_type = antal_type.set_index('type')
    # antal_type.index.name = 'Volumen'
    # st.dataframe(antal_type.T)
    
    st.divider()



    st.write('Sække til ombytning:')
    #antal_sække = df[df['sæk']].groupby(['adresse','postnr', 'beholder', 'fremsætter'])['antal'].sum(numeric_only=True).reset_index()
    sække = groupby('sæk', 'fremsætter')
    st.write(f' Antal: {sække["antal"].sum()}')
    if st.checkbox('Vis Adresser', key='1', value=True):
            
        st.dataframe(sække, use_container_width=True, hide_index=True)
        st.divider()

    st.write('Fremsætninger:')
    #antal_fremsætninger = df[df['fremsætter']].groupby(['adresse', 'postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
    fremsætninger = groupby('fremsætter')
    # st.write(f' Antal: {df["fremsætter"].sum()}')
    st.write(f' Antal fremsætninger: {fremsætninger["antal"].sum()}')
    if st.checkbox('Vis Adresser', key='2', value=False):
        st.dataframe(fremsætninger, use_container_width=True, hide_index=True)
        

    

if __name__ == "__main__":
    pass