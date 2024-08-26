import streamlit as st
import pandas as pd
import mymapslinks as mml
#from pathlib import Path
from enum import Enum
import logging
#import re
# from frekvens import næste_tømningsdag, find_frekvens
# from menupunkt import menupunkt_indeks, menupunkter
# from lillebil import find_adresse, hent_tømninger, volumen, hent_info, LILLEBIL_DATA
from materiel import *

if __name__ == "__main__":
    logger = logging.getLogger('lillebil_app')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    File_handler = logging.FileHandler('lillebil_app.log')
    File_handler.setFormatter(formatter)
    logger.addHandler(File_handler)

class Mypage(Enum):
    TABLE = 0
    INFO = 1
    SEARCH = 2
    VIS_DETAILJER = 3
    TEST = 4
    DEBUG = 5


@classmethod
def formatted_options(cls):
    return [x.name for x in cls]



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
    session_state[page] = Mypage.TABLE.value

def init_session_state():
    if page not in session_state:
        update_session_state(menu_key, menupunkter[menupunkt_indeks])
        update_session_state(page, Mypage.TABLE.value)

def menupunkt():
    return session_state[menu_key]

def vis_session_state():
    st.write(session_state)

def vis_data():
    valgt_menupunkt = menupunkt()
    st.write(f'## {valgt_menupunkt} Uge {nummeret_på_ugen}')
    st.write('### Tømninger:')
    logger.info(f'Viser tømninger for {session_state[menu_key]}')
    #df = hent_tømninger(hent_menupunkt())
    hent_tømninger(menupunkt())
    df = hent_info()
    st.dataframe(df, use_container_width=True, hide_index=True)
    if st.checkbox('Debug', key='debug', value=False):
        st.data_editor(LILLEBIL_DATA)    


def vis_adresse():
    try:
         
        resultat = find_adresse(session_state['search'])
    
    except ValueError as e:
        #st.write(e)
        st.write(f'Ingen adresse fundet: {session_state["search"]}')
        return
     
    for row in resultat.itertuples():
        col1,col2 = st.columns([1,2])
        col1.write(row.adresse)
        col2.button('Vis detaljer', key= row.id, on_click= update_details, args=(row,))
        dag, dato = næste_tømningsdag(row.tur)
        #st.write(f'Tømmes {find_frekvens(row.tur)}')
        col1.write(f'Næste tømning: {dag} {dato}')
        st.markdown('---')

def update_details(row):
    update_session_state(page, Mypage.VIS_DETAILJER.value)
    update_session_state(display_item, row)

def vis_details():
    row = session_state[display_item]
    adresse = row.adresse
    st.subheader(adresse, anchor='details',divider=True)
    

    st.write(f'Følgende materiel er tilmeldt adressen:')
    resultat = find_adresse(adresse)
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
    dag, dato = næste_tømningsdag(row.tur)
    st.write(f'Næste tømning: {dag} {dato}')
    #st.write(f'Næste tømning: {næste_tømningsdag(row.tur)}')
    st.write(f'Tømmes {find_frekvens(row.tur)}')


def vis_info():
    st.write(f'## {session_state[menu_key]}')
    st.write('### Info:')
    #antal_alt= hent_tømninger(hent_menupunkt())['antal'].sum()
    antal_alt = hent_info(sum=True)
    st.write(f'Antal tømninger: {antal_alt}')
    
    st.text('Fordelt på følgende størrelser(liter):')
    #antal = volumen(hent_menupunkt(),'type')
    antal = volumen('type')
    st.dataframe(antal)
 
    st.divider()

    #st.write('Sække til ombytning:')
    #antal_sække = df[df['sæk']].groupby(['adresse','postnr', 'beholder', 'fremsætter'])['antal'].sum(numeric_only=True).reset_index()
    sække = hent_info('sæk', 'fremsætter')

    st.write('Sække til ombytning:')
    st.write(f' Antal: {sække["antal"].sum()}')
        #st.dataframe(sække, use_container_width=True, hide_index=True)
    if not sække.empty:
        #st.divider()
        if st.checkbox('Vis Adresser', key='1', value=True):
            
            st.dataframe(sække, use_container_width=True, hide_index=True)
            st.divider()

    st.write('Fremsætninger:')
    #antal_fremsætninger = df[df['fremsætter']].groupby(['adresse', 'postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
    fremsætninger = hent_info('fremsætter')
    # st.write(f' Antal: {df["fremsætter"].sum()}')
    st.write(f' Antal fremsætninger: {fremsætninger["antal"].sum()}')
    if st.checkbox('Vis Adresser', key='2', value=False):
        st.dataframe(fremsætninger, use_container_width=True, hide_index=True)
        

    
def se_kort():
    link = mml.get_map_url(session_state[menu_key])
    st.markdown(f'- Se placering på [kort]({link})')

def setup_sidebar():
    sidebar.title('Menu')
    sidebar.selectbox(
        "Vælg Dag og Uge",
        key= 'dag_uge',
        options=menupunkter,

        index=menupunkt_indeks,
        on_change=update_menu_key
        )
    
    with sidebar.expander('Vis', expanded=True):
        st.button('Vis Info', key='info', on_click=update_session_state, args=(page, Mypage.INFO.value))
        st.button('Vis Tømninger', key='table', on_click=update_session_state, args=(page, Mypage.TABLE.value))
        
        se_kort()
    
    with sidebar.expander('Søg', expanded=False):
        #st.text_input('Søg efter adresse', key='search', on_change=update_session_state, args=(page, Mypage.SEARCH.value))
        st.text_input('Søg på adresse', key='search', on_change=update_session_state, args=(page, Mypage.SEARCH.value))

        if st.button('Søg', key='search_button', on_click=update_session_state, args=(page, Mypage.SEARCH.value)):# args=(session_state['search'],)):
            #find_address(session_state['search'])
            pass
    with sidebar.expander('Debug', expanded=False):
        st.button('Vis Session State', key='session_state', on_click=update_session_state, args=(page, Mypage.DEBUG.value))
        
if __name__ == "__main__":

        init_session_state()
        setup_sidebar()

        if session_state[page] == Mypage.SEARCH.value:
            vis_adresse()
        if session_state[page] == Mypage.TABLE.value:
            vis_data()
        elif session_state[page] == Mypage.INFO.value:
            vis_info()
        elif session_state[page] == Mypage.VIS_DETAILJER.value:
            vis_details()
        elif session_state[page] == Mypage.DEBUG.value:
            vis_session_state()
        else:
             st.write('No Matching Page')



        
                    