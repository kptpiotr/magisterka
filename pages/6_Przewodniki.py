"""Simple dashboards with Streamlit"""
import datetime
import os
import time

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector
from datetime import datetime
from sorcery import dict_of

import db
import utils
from generate_guide import GuideGenerator

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'

guides_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'guides'))
COMPANY_NAME = 'WZK'


def get_docx_files(directory):
    docx_files = [f for f in os.listdir(directory) if f.endswith('.docx')]
    return docx_files


def get_tool_info(tool_number):
    print(f"TOOL NUMBER: {tool_number}")
    if tool_number is not None and tool_number != " ":
        tool_info = db.get_tool_by_number(tool_number)
    else:
        return None, None

    if tool_info is not None:
        return tool_info[0], tool_info[1]
    else:
        return None, None


def add_tools_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add 2 columns to a dataframe with only tool number. Download Tool name and info from a db
    :param df: Dataframe with operations and tool number column
    :return: Dataframe with complete tool info
    """
    # df['Nazwa narzędia'] = None
    # df['Opis narzędzia'] = None

    df[['Nazwa narzędia', 'Opis narzędzia']] = df['Numer narzędzia'].apply(lambda x: pd.Series(get_tool_info(x)))

    return df


def save_guide(production_guide_number, part_number, part_name, blueprint_number, trade_order_number,
               amount, deadline, info, material_name, material_type, material_standard,
               material_additional_info, order_number, pl_number, unit, standard, waste, dimensions,
               batch_number, melt_number, pz_number, operations_df, company_name=COMPANY_NAME):
    generator = GuideGenerator('template.docx')

    # NAZWA_FIRMY = company_name
    # NR = production_guide_number
    # NR_CZESCI = part_number
    # NAZWA_CZESCI = part_name
    # NR_ZAMOW = order_number
    # NR_RYS = blueprint_number
    # NR_ZLECENIA = trade_order_number
    # NR_PL = pl_number
    # AMOUNT = amount
    # UWAGA = info
    # TERMIN_DOSTAWY = deadline
    # DATA_EMISJI = datetime.now().date()
    # J = unit
    # NORMA = standard
    # ODPAD = waste
    # WYMIARY = dimensions
    # NR_PARTII = batch_number
    # NR_WYTOPU = melt_number
    # NR_PZ = pz_number
    # MATERIAL = material_name
    # GATUNEK = material_type
    # NORMA_MAT = material_standard
    # DOD_MAT = material_additional_info
    #
    # to_replace = dict_of('NAZWA_FIRMY', 'NR', 'NR_CZESCI', 'NR_CZESCI', 'NAZWA_CZESCI',
    #                   'NR_ZAMOW', 'NR_RYS', 'NR_ZLECENIA', 'NR_PL', 'AMOUNT',
    #                   'UWAGA', 'TERMIN_DOSTAWY', 'DATA_EMISJI', 'MATERIAL', 'J',
    #                   'NORMA', 'ODPAD', 'WYMIARY', 'NR_PARTII', 'NR_WYTOPU',
    #                   'NR_PZ', 'GATUNEK', 'NORMA_MAT', 'DOD_MAT')

    to_replace = {
        "NAZWA_FIRMY": company_name,
        "NR_P": production_guide_number,
        "NR_CZESCI": part_number,
        "NAZWA_CZESCI": part_name,
        "NR_ZAMOW": order_number,
        "NR_RYS": blueprint_number,
        "NR_ZLECENIA": trade_order_number,
        "NR_PL": pl_number,
        "AMOUNT": amount,
        "UWAGA": info,
        "TERMIN_DOSTAWY": deadline,
        "DATA_EMISJI": str(datetime.now().date()),
        "J_M": unit,
        "NORMA": standard,
        "ODPAD": waste,
        "WYMIARY": dimensions,
        "NR_PARTII": batch_number,
        "NR_WYTOPU": melt_number,
        "NR_PZ": pz_number,
        "MATERIAL": material_name,
        "GATUNEK": material_type,
        "NORMA_MAT": material_standard,
        "DOD_MAT": material_additional_info
    }

    generator.replace(to_replace)
    generator.add_header_table()

    # Add new blank columns to the df
    new_cols_list = ['Nr zn. wykon. Data rozp. Data zak.',
                     'ODB 1 SZT. KJ', 'MISTRZ', 'DOBRE', 'ZŁE', 'KJ'
                     'Uwagi', ]
    operations_df = pd.concat([operations_df, pd.DataFrame(columns=new_cols_list)])

    generator.add_process_tables(operations_df)

    generator.add_ending()

    # data = {
    #     'Column A': np.random.rand(5),
    #     'Column B': np.random.randint(1, 100, 5),
    #     'Column C': np.random.choice(['A', 'B', 'C', 'D'], 5),
    #     'Column D': np.random.randn(5)
    # }
    # test_df = pd.DataFrame(data)

    tools_df = operations_df.loc[operations_df['Numer narzędzia'].notna(), ['Oper/czyn', 'Numer narzędzia']]
    # tools_df = tools_df.rename(columns={'Oper/czyn': 'newName1'})
    tools_df = add_tools_info(tools_df)

    print(tools_df)
    tools_df = tools_df.loc[tools_df['Opis narzędzia'].notna()]
    generator.add_tools_page(tools_df, company_name, production_guide_number, part_number, str(datetime.now().date()))

    materials_data = {
        'Nr oper': ['000'],  # ValueError: If using all scalar values, you must pass an index
        'Nr materiału': [material_name],
        'Nazwa materiału': [material_name],
        'Nr partii': [batch_number],
        'Jed m.': ['szt.'],
        'Norma': [1],
        'Norma przewodnik': [1],
        'Wydano': ['']
    }

    materials_df = pd.DataFrame(materials_data)

    generator.add_materials_page(materials_df, company_name, production_guide_number, part_number, str(datetime.now().date()))

    generator.save_file(f'{guides_folder}/{production_guide_number}.docx')


st.set_page_config(
    page_title="Przewodniki",
    page_icon="✅",
    layout="wide",
)

# Page title
st.title("Przewodniki")

# creating a single-element container
placeholder = st.empty()
if utils.get_auth_status():
    with placeholder.container():

        st.markdown("### Generowanie przewodnika")
        with st.expander("Rozwiń"):
            production_order = st.text_input("Zlecenie produkcyjne")

            with st.form('guide'):
                production_guide_number = st.text_input("Nr przewodnika")
                part_number = st.text_input("Nr części", value="0")
                part_name = st.text_input("Nazwa części", value="0")
                blueprint_number = st.text_input("Nr rys.")
                trade_order_number = st.text_input("Numer zlecenia", value="0")
                amount = st.text_input("Ilość", value="0")
                deadline = st.text_input("Termin dostawy", value="0")
                info = st.text_input("Uwaga")

                # -------------------------
                material_name = st.text_input("Nazwa materiału", value="0")
                material_type = st.text_input("Gatunek materiału", value="0")
                material_standard = st.text_input("Norma materiału", value="0")
                material_additional_info = st.text_input("Dodatkowe wymagania materiału", value="0")

                # ----------------------
                order_number = st.text_input("Numer zamówienia", value="")
                pl_number = st.text_input("Nr pl", value="")
                unit = st.selectbox("Jednostka miary", ["mm", "cal"])
                standard = st.text_input("Norma", value="0")
                waste = st.text_input("Odpad", value="0")
                dimensions = st.text_input("Wymiary", value="0")
                batch_number = st.text_input("Nr partii", value="0")
                melt_number = st.text_input("Nr wytopu", value="0")
                pz_number = st.text_input("Nr pz", value="0")

                st.write("Dodawanie operacji")

                operations_df_blank = pd.DataFrame(
                    columns=['Oper/czyn', 'Sym. oper.', 'Nazwa', "Komentarz", "Czas", "Numer narzędzia"])
                operations_df = st.data_editor(operations_df_blank, num_rows='dynamic')

                submit = st.form_submit_button('Dodaj')
            if submit:
                save_guide(production_guide_number, part_number, part_name, blueprint_number, trade_order_number,
                           amount, deadline, info, material_name, material_type, material_standard,
                           material_additional_info, order_number, pl_number, unit, standard, waste, dimensions,
                           batch_number, melt_number, pz_number, operations_df)
                st.info('Dodano przewodnik', icon="ℹ️")

        st.divider()

        st.markdown("### Eksport przewodników")
        
        # Specify the directory where .docx files are located
        docx_files = get_docx_files(guides_folder)

        selected_file = st.selectbox("Wybierz przewodnik do pobrania", docx_files)

        print(selected_file)

        if selected_file:
            # Provide a download link
            # download_link = f"[Pobierz przewodnik {selected_file}]({guides_folder}/{selected_file})"

            with open(guides_folder + '/' + selected_file, 'rb') as f:
                st.download_button('Pobierz przewodnik', f, file_name=selected_file)


else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
