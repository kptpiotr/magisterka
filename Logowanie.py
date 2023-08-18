import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

import db
import utils

st.set_page_config(
    page_title="Logowanie",
    page_icon="👋",
)
# Clear the cache (if started from other page that start.py)
st.cache_data.clear()

# Login
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Streamlit Authenticator addon only accepts this format... Better to use a databaes than a yaml file
auth_users_list = utils.create_auth_users_list()

authenticator = stauth.Authenticate(
    auth_users_list,
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# TODO uncomment to enable logging in
# st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = authenticator.login('Logowanie', 'main')
# print(f'DANE LOGOWANIA: {st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"]}')

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'

# print(st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"])
# Get user access level from db by username
st.session_state["role"] = db.get_user_role_by_username(st.session_state["username"])

try:
    if st.session_state["authentication_status"]:
        st.write(f'Zalogowano jako: *{st.session_state["name"]}*')
        st.write(f'Twój poziom dostępu: {str(st.session_state["role"])}')
        st.write(f'Wersja demonstracyjna. Brak konieczności logowania.')
        authenticator.logout('Wyloguj', 'main', key='unique_key')

    elif st.session_state["authentication_status"] is False:
        st.error('Niepoprawna nazwa użytkownika lub hasło!')

        # Clear the cache
        st.cache_data.clear()

    elif st.session_state["authentication_status"] is None:
        st.warning('Proszę podać nazwę użytkownika i hasło')

        # Clear the cache after logout
        st.cache_data.clear()
except KeyError:
    pass

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
