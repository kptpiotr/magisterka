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


def add_machine(machine_name, machine_type, machine_work_cost_hour):
    created_at, created_by = utils.get_info()

    db.insert_machine(created_at, created_by, machine_name, machine_type, machine_work_cost_hour)


st.set_page_config(
    page_title="Maszyny",
    page_icon="✅",
    layout="wide",
)

# Page title
st.title("Maszyny")

# creating a single-element container
placeholder = st.empty()
if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Łączna liczba maszyn",
            value=f"{db.get_number_of_machines()}",
        )

        current_date = datetime.datetime.now().date()
        today = pd.Timestamp(current_date).date()

        st.divider()

        st.markdown("### Przegląd maszyn")

        st.dataframe(db.get_machines(), use_container_width=True)
        st.divider()

        st.markdown("### Dodaj maszynę")
        with st.expander("Rozwiń"):
            with st.form('machine'):
                machine_name = st.text_input("Nazwa")
                machine_type = st.text_input("Rodzaj")
                machine_work_cost_hour = st.number_input("Koszt na godzinę")
                submit = st.form_submit_button('Dodaj')
            if submit:
                add_machine(machine_name, machine_type, machine_work_cost_hour)
                st.info('Dodano maszynę', icon="ℹ️")

        st.divider()

        st.markdown("### Wykorzystanie maszyn")
        with st.form('machine_gantt'):
            machines_df = db.get_machines()
            machines_list = machines_df.index.unique()

            selected_machine = st.selectbox(options=machines_list, label='Wybrana maszyna (ID)')
            start = st.date_input("Początek")
            finish = st.date_input("Koniec")

            submit = st.form_submit_button('Pokaż wykorzystanie maszyny')

            if submit:
                selected_actions_df = db.get_machines_actions_between_dates(selected_machine, start, finish)
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
