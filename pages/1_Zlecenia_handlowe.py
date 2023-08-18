"""Simple dashboards with Streamlit"""

import streamlit as st
import db
import utils
import mysql.connector
from mysql.connector import errorcode

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'


def add_trade_order(name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost,
                    price):
    # TODO add the data to the DB
    created_at, created_by = utils.get_info()

    db.insert_trade_order(created_at, created_by, 'Oczekujące', name, order_number, order_type, client, material,
                          number_ordered, number_to_make, deadline, comment, cost, price)


st.set_page_config(
page_title="Zlecenia handlowe",
page_icon="✅",
layout="wide",
)


# Page title
st.title("Zlecenia handlowe")

# creating a single-element container
placeholder = st.empty()

if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Zlecenia do zamknięcia w ciągu najbliższych 7 dni:",
            value=f"{db.get_trade_orders_number_next_7d()}",
        )

        kpi20.metric(
            label="Oczekujące zlecenia handlowe",
            value=f"{db.get_awaiting_trade_orders_number()}",
        )

        st.divider()

        st.markdown("### Zlecenia handlowe")

        original_trade_orders_df = db.get_trade_orders()

        hide_finished_orders = st.checkbox('Ukryj zakończone')

        with st.form('modify_orders_form'):
            if hide_finished_orders:
                original_trade_orders_df = original_trade_orders_df.loc[original_trade_orders_df['Status'] != 'Zakończone']

            modified_trade_orders_df = st.data_editor(original_trade_orders_df, column_config={
                    "Rodzaj": st.column_config.SelectboxColumn(
                        "Rodzaj",
                        help="Rodzaj zlecenia",
                        width="medium",
                        options=[
                            "Zlecenie zewnętrzne",
                            "Zlecenie wewnętrzne",
                        ],
                    ),
                    "ID": st.column_config.Column(
                        "ID",
                        help="ID zlecenia",
                        width="medium",
                        disabled=True,
                    ),
                    "Utworzone przez": None
                }
            )

            # Get edited rows and update the DB
            changed_rows_list = utils.get_edited_records(original_trade_orders_df, modified_trade_orders_df)

            if st.form_submit_button("Zapisz zmiany") and len(changed_rows_list) > 0:
                print(changed_rows_list)

                rows_to_update = modified_trade_orders_df.loc[modified_trade_orders_df.index.isin(changed_rows_list)]
                print(rows_to_update)

                # Update the edited rows in the db
                for row in list(rows_to_update.itertuples(index=True, name=None)):
                    db.replace_trade_order(tuple(row))

                st.info("Zapisano")

        st.divider()

        st.markdown("### Dodaj zlecenie handlowe")

        with st.expander('Rozwiń'):
            with st.form('order'):
                # TODO finish, what else info is needed? Jedno zlecenie handlowe na jedno produkcyjne czy kilka produkcyjnych na 1 handlowe?
                name = st.text_input("Nazwa zlecenia")
                order_number = st.number_input("Numer zlecenia", min_value=0, step=1)
                order_type = st.selectbox("Rodzaj zlecenia", ["Zlecenie zewnętrzne", "Zlecenie wewnętrzne"])
                client = st.text_input("Kontrahent")
                material = st.text_input("Materiał")
                number_ordered = st.number_input("Liczba zlecona", min_value=0, step=1)
                number_to_make = st.number_input("Liczba do uruchomienia", min_value=0, step=1)
                deadline = st.date_input("Planowana data dostarczenia")
                comment = st.text_area("Uwagi")

                cost = st.number_input("Techniczny koszt wytworzenia [zł]", min_value=0, step=1)
                price = st.number_input("Wartość zlecenia [zł]", min_value=0, step=1)

                submit = st.form_submit_button('Dodaj')
            if submit:
                try:
                    add_trade_order(name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost, price)
                    st.info('Dodano zlecenie handlowe', icon="ℹ️")
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        st.error('Istnieje już zlecenie handlowe o tym numerze!')
                    else:
                        st.error(f"BŁĄD: {err}")
else:
    st.warning("Proszę się zalogować!")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)