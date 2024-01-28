import streamlit as st
import pandas as pd
import mymapslinks as mml
from pathlib import Path
from enum import Enum
import re
#from tyvetools import extract_house_number, extract_street_city_country3
from string import ascii_lowercase
from random import choice
#from swingwers import naste_tomning, return_skema
from t20 import *

class Mypage(Enum):
    TABLE = 0
    INFO = 1
    SEARCH = 2
    VIS_DETAILJER = 3


@classmethod
def formatted_options(cls):
    return [x.name for x in cls]

# --------------------------------------------- Config ---------------------------------------------

csv_folder = Path.cwd() / 'nydata'
csv_files = [file for file in csv_folder.glob('*.csv')]
csv_dict =  {file.stem: file for file in csv_files}

csv_info = Path.cwd() / 'data'
csv_info_files = [file for file in csv_info.glob('*.csv')]
csv_info_dict =  {file.stem: file for file in csv_info_files}

# --------------------------------------------- Config ---------------------------------------------
#lookup
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
        update_session_state(menu_key, list(csv_dict.keys())[0])
        update_session_state(page, Mypage.TABLE.value)


def random_string(length=8):
        """Create a random ASCII string using the specified length

        Args:
            length (int, optional): The desired length for the random string. Defaults to 8.

        Returns:
            str: The random string
        """
        return "".join(choice(ascii_lowercase) for _ in range(length))


def find_address():
    address = session_state['search']
    adresse_fundet = []
    adresse_regex = re.compile(rf'{address}', re.IGNORECASE)
    for df in csv_info_dict.values():
        df = pd.read_csv(df)
        for row in df.itertuples():
            if adresse_regex.findall(row.adresse):
                adresse_fundet.append(row)
    #df =pd.DataFrame(adresse_fundet)

    #st.dataframe(adresse_fundet)    
    update_session_state(page, Mypage.SEARCH.value)
    update_session_state(search_result, adresse_fundet)

def find_address1(address):
    adresse_fundet = []
    adresse_regex = re.compile(rf'{address}', re.IGNORECASE)
    for df in csv_info_dict.values():
        df = pd.read_csv(df)
        for row in df.itertuples():
            if adresse_regex.findall(row.adresse):
                adresse_fundet.append(row)
    st.dataframe(adresse_fundet)    

def find_address2(address):
    adresse_regex = re.compile(rf'{address}', re.IGNORECASE)
    for df in csv_info_dict.values():
        df = pd.read_csv(df)
        for row in df.itertuples():
            if adresse_regex.findall(row.adresse):
                col1,col2 = st.columns([1,2])
                col1.write(row.adresse)
                col2.button('Vis detaljer', key= random_string() , on_click= update_details, args=(row,))
                #st.write(f'Tømmes {find_dag_uge(row.tur)}')
                st.write(f'Tømmes {return_skema(row.tur)}')
                st.markdown('---')

def show_adresse1(row):
    result = session_state[search_result]
    result = pd.DataFrame(result)
    result = result.drop_duplicates(subset=['adresse'])
    for row in result.itertuples():
        col1,col2 = st.columns([1,2])
        col1.write(row.adresse)
        col2.button('Vis detaljer', key= random_string() , on_click= update_details, args=(row,))
        st.write(f'Tømmes {return_skema(row.tur)}')
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
    gade, postnr,by, land = row.adresse.split(',')
    st.subheader(gade, anchor='details',divider=True)
    

    st.write(f'Følgende beholdere er tilmeldt:')
    result = session_state[search_result]
    result = pd.DataFrame(result)
    result = result.groupby(['adresse', 'beholder'])['antal'].sum()


    col3, col4 = st.columns(2)
    with col3:
        st.markdown('Beholder:')
    with col4:
        st.markdown('Antal:')
    col1, col2 = st.columns(2)
    for beholder in result.loc[adresse].index:
         
         antal = result.loc[adresse][beholder]
         with col1:
            st.write(f'{beholder}')
         with col2:
            st.write(f'{antal:>}')
         #st.markdown('---')
    #st.dataframe(result.loc[adresse])
         #st.write(f'Beholder: {beholder} Antal: {antal}')
    st.write(f'Næste tømning: {naste_tomning(row.tur)}')
    

def vis_session_state():
    st.write(session_state)



def load_data():
    st.write('### Tømninger:')
    st.write(f'## {format_menu_key()}')
    file = csv_dict[session_state[menu_key]]
    df = pd.read_csv(file)
    df = extract_street_city_country3(df)
    df = extract_house_number(df)
    df['postnr'] = df['postnr'].astype(str)
    dff = df.groupby(['street', 'postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
    st.dataframe(dff, use_container_width=True, hide_index=True)


def load_info():
    st.write('### Info:')
    st.write(f'## {format_menu_key()}')
    file = csv_info_dict[session_state[menu_key]]

    df = pd.read_csv(file)

    df = pd.read_csv(file)
    antal = df['antal'].sum()
    st.write(f'Antal: {antal}')
    
    st.text('Fordelt på følgende størrelser(liter):')
    antal_type = df.groupby(['type'])[["antal"]].sum(numeric_only=True).reset_index()
    antal_type = antal_type.set_index('type')
    st.write(antal_type.T)
    st.divider()

    st.write('Sække til ombytning:')
    antal_sække = df[df['sæk']].groupby(['gade', 'nr','postnr', 'beholder', 'fremsætter'])['antal'].sum(numeric_only=True).reset_index()
    st.write(f' Antal: {df["sæk"].sum()}')
    if st.checkbox('Vis Adresser', key='1', value=True):
            
        st.dataframe(antal_sække, use_container_width=True, hide_index=True)
        st.divider()

    st.write('Fremsætninger:')
    antal_fremsætninger = df[df['fremsætter']].groupby(['gade', 'nr','postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
    st.write(f' Antal: {df["fremsætter"].sum()}')
    if st.checkbox('Vis Adresser', key='2', value=False):
        st.dataframe(antal_fremsætninger, use_container_width=True, hide_index=True)
        

    # my_df = 'gade, nr, postnr, beholder, antal'.split(', ')
    # df = df[my_df]
    # st.dataframe(df, use_container_width=True, hide_index=True)

     
def format_menu_key():
    return ' '.join(session_state[menu_key].split("_")).title()
def se_kort():
    link = mml.get_link(session_state[menu_key])
    st.markdown(f'- Se kort over [placering]({link})')

def setup_sidebar():
    sidebar.title('Menu')
    menu = sidebar.selectbox(
        "Vælg Dag og Uge",
        key= 'dag_uge',
        options=csv_dict,
        on_change=update_menu_key)
    
    with sidebar.expander('Vis Tømninger', expanded=True):
        st.button('Vis Info', key='info', on_click=update_session_state, args=(page, Mypage.INFO.value))
        st.button('Vis Tømninger', key='table', on_click=update_session_state, args=(page, Mypage.TABLE.value))
        
        se_kort()
    
    with sidebar.expander('Søg', expanded=False):
        #st.text_input('Søg efter adresse', key='search', on_change=update_session_state, args=(page, Mypage.SEARCH.value))
        st.text_input('Søg efter adresse', key='search', on_change=find_address,)# args=(session_state['search'],))

        if st.button('Søg', key='search_button', on_click=find_address,):# args=(session_state['search'],)):
            #find_address(session_state['search'])
            pass


if __name__ == "__main__":

        init_session_state()
        setup_sidebar()

        if session_state[page] == Mypage.TABLE.value:
            #st.dataframe(load_data(), use_container_width=True, hide_index=True)
            load_data()
        elif session_state[page] == Mypage.INFO.value:
            #st.dataframe(load_info(), use_container_width=True, hide_index=True)
            load_info()
        elif session_state[page] == Mypage.SEARCH.value:
            #vis_session_state()
            #find_address2(session_state['search'])
            show_adresse1('dummy')
        elif session_state[page] == Mypage.VIS_DETAILJER.value:
            vis_details()
        else:
            st.write('No Matching Page')


        
                    