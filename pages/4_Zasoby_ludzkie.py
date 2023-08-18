"""Simple dashboards with Streamlit"""
import datetime
import time

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import mysql.connector

import db
import utils

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'


def add_employee(worker_name, worker_surname, worker_work_cost_hour, worker_type):
    created_at, created_by = utils.get_info()

    db.insert_employee(created_at, created_by, worker_name, worker_surname, worker_work_cost_hour, worker_type)


def get_attendance_df():
    attendance_df = db.get_employees()  # ['ID', 'Imię', 'Nazwisko', 'Rodzaj']
    attendance_df = attendance_df[['Imię', 'Nazwisko', 'Rodzaj']]

    current_date = datetime.datetime.now().date()
    attendance_df['Data'] = pd.Timestamp(current_date).date()
    attendance_df['Zmiana'] = 1
    attendance_df['Obecność'] = True
    attendance_df['Komentarz'] = None

    return attendance_df


def add_attendance(df):
    created_at, created_by = utils.get_info()

    for index, row in df.iterrows():
        db.add_record_to_attendance_list(created_at, created_by, row['Data'], row['Zmiana'], index, row['Obecność'],
                                         row['Komentarz'])


st.set_page_config(
    page_title="Zasoby ludzkie",
    page_icon="✅",
    layout="wide",
)

# Page title
st.title("Zasoby ludzkie")

# creating a single-element container
placeholder = st.empty()
if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Łączna liczba pracowników produkcji",
            value=f"{db.get_number_of_employees()}",
        )

        current_date = datetime.datetime.now().date()
        today = pd.Timestamp(current_date).date()

        kpi20.metric(
            label="Liczba nieobecnych pracowników",
            value=f"{db.get_number_of_absent_employees(today, 1)}",
        )

        st.divider()

        st.markdown("### Lista obecności")

        with st.form('attendance_list'):
            modified_attendance_df = st.data_editor(get_attendance_df(), use_container_width=True, column_config={
                "Data": st.column_config.DateColumn(disabled=True),
                "_index": None,
                "Imię": st.column_config.Column(disabled=True),
                "Nazwisko": st.column_config.Column(disabled=True),
                "Rodzaj": st.column_config.Column(disabled=True)
            })

            attendance_submit = st.form_submit_button('Zapisz')
            if attendance_submit:
                try:
                    add_attendance(modified_attendance_df)
                    st.info('Zapisano listę obecności', icon="ℹ️")

                except mysql.connector.Error as err:
                    if err.errno == 1062:
                        st.error("Obecność już była sprawdzona!")
                    else:
                        # Handle other MySQL errors
                        print(f"MySQL error: {err}")
        st.divider()

        st.markdown("### Przegląd pracowników")

        with st.expander("Rozwiń"):
            workers_df = st.data_editor(db.get_employees(), num_rows='dynamic', column_config={
                "Utworzone przez": None,
                "Utworzono": None,
                "Rodzaj": st.column_config.SelectboxColumn(
                    "Rodzaj",
                    options=["Ślusarz", "Operator CNC", "Programista CNC", "Spawacz",
                             "Kontroler jakości"],
                )
            })

            workers_submit = st.button('Aktualizuj')
            if workers_submit:
                db.update_employees(workers_df)
                st.info('Zaktualizowano pracowników', icon="ℹ️")

        st.divider()

        st.markdown("### Dodaj pracownika")
        with st.expander("Rozwiń"):
            with st.form('worker'):
                worker_name = st.text_input("Imię")
                worker_surname = st.text_input("Nazwisko")
                worker_work_cost_hour = st.number_input("Koszt na godzinę")
                # worker_type = st.text_input("Typ")
                worker_type = st.selectbox("Typ", ["Ślusarz", "Operator CNC", "Programista CNC", "Spawacz",
                                                   "Kontroler jakości"])

                submit = st.form_submit_button('Dodaj')
            if submit:
                add_employee(worker_name, worker_surname, worker_work_cost_hour, worker_type)
                st.info('Dodano pracownika', icon="ℹ️")

        st.markdown("### Zadania przypisane do pracowników")
        with st.form('employee_gantt'):
            employees_df = db.get_employees()
            employees_list = employees_df.index.unique()

            selected_employee = st.selectbox(options=employees_list, label='Wybrany pracownik (ID)')
            start = st.date_input("Początek")
            finish = st.date_input("Koniec")

            submit = st.form_submit_button('Pokaż zadania pracowników')

            if submit:
                selected_actions_df = db.get_employees_actions_between_dates(selected_employee, start, finish)
                print(selected_actions_df)

                fig = px.timeline(selected_actions_df, x_start="Początek", x_end="Koniec", y="Zlecenie produkcyjne")

                fig.update_yaxes(autorange="reversed", type="category")
                st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
