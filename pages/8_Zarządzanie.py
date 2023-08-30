"""
For admins only.
Create new user
"""
from datetime import date

import streamlit as st
import db
import utils
import streamlit_authenticator as stauth

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'


def add_user(name, surname, email, username, password_hash, role):
    created_at, created_by = utils.get_info()

    db.insert_user(created_at, created_by, name, surname, email, username, password_hash, role)


def update_holidays(holidays_df):
    created_at, created_by = utils.get_info()

    db.update_holidays(created_at, created_by, holidays_df)


st.set_page_config(
page_title="Zarządzanie",
page_icon="✅",
layout="wide",
)


# Page title
st.title("Zarządzanie")

# creating a single-element container
placeholder = st.empty()
if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Użytkownicy",
            value=f"{db.get_number_of_users()}",
        )

        st.divider()

        # st.write(f"TEST: {st.session_state['role']}")

        st.markdown("### Użytkownicy")

        # TODO Add 'last active' column
        st.dataframe(db.get_users(), column_config={
            "Email": st.column_config.Column(
                "Email",
                width="medium",
            ), "Hash": None
        }, use_container_width=True)

        st.divider()

        st.markdown("### Dodaj użytkownika")

        if utils.get_user_role() == 'Administrator':
            with st.expander("Rozwiń"):
                with st.form('new_user'):
                    name = st.text_input("Imię")
                    surname = st.text_input("Nazwisko")
                    email = st.text_input("Email")
                    username = st.text_input("Nazwa użytkownika")
                    password = st.text_input("Hasło", type='password')
                    password_hash = stauth.Hasher([password]).generate()
                    role = st.selectbox("Rodzaj", ["Administrator", "Specjalista ds. sprzedaży", "Dyrektor"])

                    new_user_submit = st.form_submit_button('Dodaj')
                    if new_user_submit:
                        add_user(name, surname, email, username, password_hash[0], role)
                        st.info('Dodano użytkownika', icon="ℹ️")

        elif utils.get_user_role() is None:
            st.write("Proszę się zalogować na stronie głównej")
        else:
            st.write("Wymagane uprawnienia administratora")

        st.markdown("### Dni wolne od pracy")

        if utils.get_user_role() == 'Administrator' or utils.get_user_role() == 'Dyrektor':
            with st.expander("Rozwiń"):
                holidays_df = st.data_editor(db.get_holidays(), num_rows='dynamic', column_config={
                "Data": st.column_config.DateColumn(
                    "Data",
                    min_value=date(2022, 1, 1),
                    max_value=date(2200, 1, 1),
                    format="DD.MM.YYYY",
                    step=1,
                ),
            }
                                             )

                holidays_submit = st.button('Aktualizuj')
                if holidays_submit:
                    update_holidays(holidays_df)
                    st.info('Zaktualizowano dni wolne od pracy', icon="ℹ️")

        else:
            st.write("Wymagane uprawnienia")
else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
