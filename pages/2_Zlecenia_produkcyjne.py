"""
For admins only.
Create new user
"""
from typing import Tuple

import numpy as np
import pandas as pd
import streamlit as st
from pandas import DataFrame

import db
import utils
from datetime import timedelta, date
import mysql.connector
from mysql.connector import errorcode

import plotly.express as px

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'


def add_production_order(name, production_order_id, trade_order_id, number, start, deadline, progress, material, status, comment):
    created_at, created_by = utils.get_info()

    db.insert_production_order(created_at, created_by, name, production_order_id, trade_order_id, number, start, deadline, progress, material, status, comment)


def update_production_order(selected_production_order, deadline, progress, status):
    db.update_production_order(selected_production_order, str(deadline), progress, status)


def calculate_gantt(df: pd.DataFrame) -> tuple[DataFrame, int, int]:
    """
    Calculate all the needed columns to create a df for a Gantt chart
    :param df:
    :return: Dataframe with needed columns only
    """
    # Get holidays from the database

    df.dropna(subset=['Numer'], inplace=True)
    empty_df_gantt['Koniec'] = None
    empty_df_gantt['Koniec'] = pd.to_datetime(empty_df_gantt['Koniec'])


    holidays = db.get_holidays()
    holidays = holidays['Data'].tolist()

    # print(f"HOLIDAYS: {holidays}")
    working_days_counter = 0
    free_days_counter = 0
    
    df['Koniec'] = None
    for index, row in df.iterrows():
        if pd.notna(row['Start']):
            df.at[index, 'Start'] = df.at[index, 'Start'].replace(hour=0, minute=1)

            # Calculete the finish date by adding duration to the starting date - consider holidays and weekends!

            finish_date, working_days_number, free_days_number = utils.calculate_finish_date(row['Start'], row['Czas trwania'], holidays)

            df.at[index, 'Koniec'] = finish_date
            df.at[index, 'Koniec'] = df.at[index, 'Koniec'] + timedelta(hours=23, minutes=59)

            working_days_counter += working_days_number
            free_days_counter += free_days_number
        else:
            # If the start date is None, calculate the start date by taking the previous task date and adding 1 day
            # print(f"{index} row is None!")
            start = df.loc[df['Numer'] == df.at[index, 'Poprzednik'], 'Koniec'].values[0] + timedelta(days=1)
            df.at[index, 'Start'] = start.replace(hour=0, minute=1)

            finish_date, working_days_number, free_days_number = utils.calculate_finish_date(start, row['Czas trwania'], holidays)

            df.at[index, 'Koniec'] = finish_date

            working_days_counter += working_days_number
            free_days_counter += free_days_number

    print(df)
    return df, working_days_counter, free_days_counter


def save_gantt(df, selected_production_order):
    print("Saving the project")
    created_at, created_by = utils.get_info()
    for index, row in df.iterrows():
        db.insert_machine_action(created_at, created_by, selected_production_order, 1, row['Start'], row['Koniec'], row['Maszyna'])
        db.insert_employee_action(created_at, created_by, selected_production_order, 1, row['Start'], row['Koniec'], row['Pracownik'])



st.set_page_config(
    page_title="Zarządzanie",
    page_icon="✅",
    layout="wide",
)

# Page title
st.title("Zlecenia produkcyjne")

# creating a single-element container
placeholder = st.empty()

if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Aktywne zlecenia produkcyjne",
            value=f"{db.get_active_production_orders_number()}",
        )

        st.divider()

        st.markdown("### Dodaj zlecenie produkcyjne")
        with st.expander('Rozwiń'):
            with st.form('order'):
                name = st.text_input("Nazwa zlecenia")
                production_order_id = st.number_input("Numer zlecenia produkcyjnego", min_value=0, step=1)
                trade_order_id = st.number_input("Numer zlecenia handlowego", min_value=0, step=1)
                number = st.number_input("Liczba", min_value=0, step=1)
                start = st.date_input("Data uruchomienia")
                deadline = st.date_input("Data zakończenia")
                progress = st.number_input("Poziom wykonania", min_value=0, max_value=100, step=1)
                material = st.text_input("Materiał")
                status = st.text_input("Status")
                comment = st.text_input("Komentarz")

                submit = st.form_submit_button('Dodaj')
            if submit:
                try:
                    add_production_order(name, production_order_id, trade_order_id, number, start, deadline, progress, material, status, comment)
                    st.info('Dodano zlecenie produkcyjne', icon="ℹ️")
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        st.error('Istnieje już zlecenie produkcyjne o tym numerze!')
                    else:
                        st.error(f"BŁĄD: {err}")

        st.divider()

        st.markdown("### Zlecenia produkcyjne")
        hide_finished_orders = st.checkbox('Ukryj zakończone', value=True)

        if hide_finished_orders:
            st.dataframe(db.get_production_orders(non_finished_only=True))
        else:
            st.dataframe(db.get_production_orders())

        st.divider()

        st.markdown("### Aktualizacja zleceń produkcyjnych")

        with st.expander('Rozwiń'):
            active_production_orders_df = db.get_production_orders(non_finished_only=True)
            active_production_orders_list = active_production_orders_df['Numer'].unique()

            selected_production_order = st.selectbox(options=active_production_orders_list, label='Wybrane zlecenie')

            with st.form('update_order'):
                deadline = st.date_input("Data zakończenia", value=active_production_orders_df.loc[active_production_orders_df['Numer'] == selected_production_order, 'Koniec'].values[0])
                progress = st.number_input("Poziom wykonania", min_value=0, max_value=100, step=1, value=active_production_orders_df.loc[active_production_orders_df['Numer'] == selected_production_order, 'Poziom wykon.'].values[0])
                status = st.text_input("Status", value=active_production_orders_df.loc[active_production_orders_df['Numer'] == selected_production_order, 'Status'].values[0])

                submit = st.form_submit_button('Aktualizuj')

            if submit:
                update_production_order(selected_production_order, deadline, progress, status)
                st.info('Zaktualizowano', icon="ℹ️")

        st.divider()
        st.markdown("### Ustalanie harmonogramu")

        selected_production_order_gantt = st.selectbox(options=active_production_orders_list, label='Wybrane zlecenie (numer)', key='gantt')

        # Create a new empty df
        with st.form('calculate_form'):
            empty_df_gantt = pd.DataFrame(columns=['Numer', 'Nazwa zadania', 'Start', 'Czas trwania', 'Poprzednik', 'Pracownik', 'Maszyna'])

            empty_df_gantt['Start'] = pd.to_datetime(empty_df_gantt['Start'])

            empty_df_gantt = empty_df_gantt.astype({"Numer": int, "Nazwa zadania": str, "Czas trwania": int, "Poprzednik": int, "Pracownik": str, "Maszyna": str})
            df_gantt = st.data_editor(empty_df_gantt, num_rows='dynamic', use_container_width=True, column_config={
                "Start": st.column_config.DateColumn(
                    "Start",
                    min_value=date(2022, 1, 1),
                    max_value=date(2200, 1, 1),
                    format="DD.MM.YYYY",
                    step=1,
                ),
                "Pracownik": st.column_config.Column("Pracownik (ID)"),
                "Maszyna": st.column_config.Column("Maszyna (ID)")
            }
                                      )

            calculate_button = st.form_submit_button('Oblicz')

            if calculate_button:
                # Calculate all the needed values
                df_gantt_calculated, working_days_counter, free_days_counter = calculate_gantt(df_gantt)

                st.session_state['df_gantt_calculated'] = df_gantt_calculated

                if df_gantt_calculated.shape[0] > 0:
                    st.write("Czasy trwania zadań:")
                    st.dataframe(df_gantt_calculated, hide_index=True, use_container_width=True, column_config={
                        "Start": st.column_config.DateColumn(
                            "Start",
                            format="DD.MM.YYYY",
                        ),
                        "Koniec": st.column_config.DateColumn(
                            "Koniec",
                            format="DD.MM.YYYY",
                        ),
                        "Pracownik": st.column_config.Column("Pracownik (ID)"),
                        "Maszyna": st.column_config.Column("Maszyna (ID)")

                }
                                 )
                    fig_color = st.selectbox(
                        'Wyświetlaj według:',
                        ('Pracownicy', 'Maszyny'))

                    if fig_color == 'Pracownicy':
                        fig = px.timeline(df_gantt_calculated, x_start="Start", x_end="Koniec", y="Nazwa zadania",
                                          color="Pracownik")
                    else:
                        fig = px.timeline(df_gantt_calculated, x_start="Start", x_end="Koniec", y="Nazwa zadania", color="Maszyna")

                    fig.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig, use_container_width=True)

                    finish_date = df_gantt_calculated['Koniec'].max().date()
                    st.write(f"Przewidywana data zakończenia projektu: {finish_date}")

        if 'df_gantt_calculated' in st.session_state:
            save_button = st.button('Zapisz projekt')
            if save_button:
                # TODO save all the data to the database
                save_gantt(st.session_state['df_gantt_calculated'], selected_production_order_gantt)
                st.info("Zapisano projekt!")

else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
