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


def add_tool(name, number, specification):
    created_at, created_by = utils.get_info()

    db.insert_tool(created_at, created_by, name, number, specification)


st.set_page_config(
page_title="Narzędzia",
page_icon="✅",
layout="wide",
)


# Page title
st.title("Narzędzia")

# creating a single-element container
placeholder = st.empty()
if utils.get_auth_status():
    with placeholder.container():

        # st.write(f"TEST: {st.session_state['role']}")

        st.markdown("### Lista narzędzi")

        # TODO Add 'last active' column
        st.dataframe(db.get_tools(), use_container_width=True)

        st.divider()

        st.markdown("### Dodaj narzędzie")

        with st.expander("Rozwiń"):
            with st.form('new_user'):
                name = st.text_input("Nazwa")
                number = st.text_input("Numer")
                specification = st.text_input("Specyfikacja")

                new_user_submit = st.form_submit_button('Dodaj')
                if new_user_submit:
                    add_tool(name, number, specification)
                    st.info('Dodano narzędzie', icon="ℹ️")


else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)