import streamlit as st
import pandas as pd
import mymapslinks as mml
from pathlib import Path
from enum import Enum
import re
from frekvens import næste_tømningsdag, find_frekvens

class Mypage(Enum):
    TABLE = 0
    INFO = 1
    SEARCH = 2
    VIS_DETAILJER = 3


@classmethod
def formatted_options(cls):
    return [x.name for x in cls]

LILLEBIL_DATA = pd.read_csv('lillebil_data.csv')
LILLEBIL_DATA['postnr'] = LILLEBIL_DATA['postnr'].astype(str)


menupunkter= ['Mandag - Lige', 'Mandag - Ulige', 'Torsdag - Lige', 'Torsdag - Ulige']
# oversæt menupunkter til kolonnenavne
oversæt = {'Mandag - Lige': 'ml', 'Mandag - Ulige': 'mu', 'Torsdag - Ulige': 'tu', 'Torsdag - Lige': 'tl'}


# --------------------------------------------- Config ---------------------------------------------
menu_key = 'menu'
# Current page
page = 'page'
# Display details
display_item = 'display_item'
# Search_result
search_result = 'search_result'

session_state = st.session_state
sidebar = st.sidebar

def update_session_state(key, value):
    session_state[key] = value

def update_menu_key():
    session_state[menu_key] = session_state['dag_uge']

def init_session_state():
    if page not in session_state:
        #update_session_state(menu_key, list(csv_dict.keys())[0])
        update_session_state(menu_key, menupunkter[0])
        update_session_state(page, Mypage.TABLE.value)



# søg på adresse
def find_adresse():
    adresse = session_state['search']
    adresse_fundet = []
    adresse_regex = re.compile(rf'{adresse}', re.IGNORECASE)
    for row in LILLEBIL_DATA.itertuples():
        if adresse_regex.findall(row.adresse):
            adresse_fundet.append(row)

    update_session_state(page, Mypage.SEARCH.value)
    update_session_state(search_result, adresse_fundet)

def vis_adresse():
    resultat = session_state[search_result]
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

def show_adresse(row):
    result = session_state[search_result]
    st.dataframe(result)


def update_details(row):
    update_session_state(page, Mypage.VIS_DETAILJER.value)
    update_session_state(display_item, row)

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
    

def vis_session_state():
    st.write(session_state)

def groupby2():
    gruppe = oversæt[session_state[menu_key]]
    df = LILLEBIL_DATA[LILLEBIL_DATA[gruppe]]
    #df['postnr'] = df['postnr'].astype(str)
    df = df.groupby(['adresse', 'postnr', 'beholder', 'vejnavn', 'husnr'])['antal'].sum(numeric_only=True)
    df = df.reset_index()
    df.sort_values(by=['vejnavn', 'husnr'], ascending=True, inplace=True)
    df.drop(columns=['vejnavn', 'husnr'], inplace=True)
    return df



def groupby(betingelse = None, info = None):

    # Betingelse : bool

    # info : str
    #
    
    # gruppe = oversæt[session_state[menu_key]]
    # df = LILLEBIL_DATA[LILLEBIL_DATA[gruppe]]

    df = gruppe()
    
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
        

    
def load_data():
    st.write(f'## {session_state[menu_key]}')
    st.write('### Tømninger:')
    df = groupby()
    #st.table(df)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.checkbox('Debug', key='debug', value=False):
        st.data_editor(LILLEBIL_DATA)    

def gruppe():
    gruppe = oversæt[session_state[menu_key]]
    df = LILLEBIL_DATA[LILLEBIL_DATA[gruppe]]
    return df

def angiv_antal(kolonnenavn):
    df = gruppe()
    #pd.DataFrame(df['type'].value_counts())
    #rename index to volumen
    df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')#.to_csv('volumen.csv', index=False)
    #df['type'].value_counts().reset_index(name='antal')
    return df[kolonnenavn].value_counts().rename_axis('volumen').reset_index(name='antal')

def load_info():
    st.write(f'## {session_state[menu_key]}')
    st.write('### Info:')

    #gruppe = oversæt[session_state[menu_key]]
    #df = LILLEBIL_DATA[LILLEBIL_DATA[gruppe]]
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
        

    
def se_kort():
    link = mml.get_link(session_state[menu_key])
    st.markdown(f'- Se placering på [kort]({link})')

def setup_sidebar():
    sidebar.title('Menu')
    sidebar.selectbox(
        "Vælg Dag og Uge",
        key= 'dag_uge',
        options=menupunkter,
        on_change=update_menu_key)
        #on_change=update_session_state, args=(menu_key, session_state['dag_uge']))
    
    with sidebar.expander('Vis', expanded=True):
        st.button('Vis Info', key='info', on_click=update_session_state, args=(page, Mypage.INFO.value))
        st.button('Vis Tømninger', key='table', on_click=update_session_state, args=(page, Mypage.TABLE.value))
        
        #se_kort()
    
    with sidebar.expander('Søg', expanded=False):
        #st.text_input('Søg efter adresse', key='search', on_change=update_session_state, args=(page, Mypage.SEARCH.value))
        st.text_input('Søg på adresse', key='search', on_change=find_adresse,)# args=(session_state['search'],))

        if st.button('Søg', key='search_button', on_click=find_adresse,):# args=(session_state['search'],)):
            #find_address(session_state['search'])
            pass


if __name__ == "__main__":

        init_session_state()
        setup_sidebar()

        if session_state[page] == Mypage.SEARCH.value:
            vis_adresse()

        if session_state[page] == Mypage.TABLE.value:
            load_data()
        elif session_state[page] == Mypage.INFO.value:
            load_info()
        elif session_state[page] == Mypage.VIS_DETAILJER.value:
            vis_details()
        else:
             st.write('No Matching Page')


        
                    