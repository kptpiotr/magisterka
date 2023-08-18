"""
Dać liste wszystkiego co jest na magazynie, wyroby gotowe zmagazynowane i kiedy, jaki ich status, wszystko z możliwością filtrowania i sortowania
Dać listę materiałów i ile ich jest, także materiały w drodze z datą zamówienia i ceną
"""
import datetime

import pandas as pd
import streamlit as st
import db
import utils
import plotly.express as px
import plotly.graph_objects as go

st.session_state["name"], st.session_state["authentication_status"], st.session_state["username"] = 'piotrbanko', True, 'piotrbanko'


def add_material_action(name, production_order_id, action_type, material, amount, date, comment):
    # TODO add the data to the DB
    created_at, created_by = utils.get_info()

    db.insert_material_action(created_at, created_by, name, production_order_id, action_type, material, amount, date,
                              comment)


def change_or_add_material_action(material_name, lower_limit, upper_limit, average_delivery_time):
    # TODO add the data to the DB
    created_at, created_by = utils.get_info()

    db.replace_material_levels(created_at, created_by, material_name, lower_limit, upper_limit, average_delivery_time)


st.set_page_config(
    page_title="Magazyn",
    page_icon="✅",
    layout="wide",
)

materials_list = db.get_materials_list()

# Page title
st.title("Magazyn materiałów")

# creating a single-element container
placeholder = st.empty()

if utils.get_auth_status():
    with placeholder.container():
        kpi10, kpi20 = st.columns(2)

        # fill in those columns with respective metrics or KPIs
        kpi10.metric(
            label="Najbliższa dostawa za:",
            value=f"{db.get_nearest_material_in()} dni",
        )

        # kpi20.metric(
        #     label="Oczekujące zlecenia handlowe",
        #     value=f"2",
        # )

        for material_info_name in db.get_materials_below_lower_limit():
            st.error(f"Zapas magazynowy poniżej progu zamawiania dla materiału: {material_info_name}. Konieczna inspekcja zamówień!")

        st.divider()

        st.markdown("### Przyjęcia i wydania wg. dni")
        selected_timespan = st.selectbox(
            'Wybierz zakres',
            ('Ostatnie 30 dni', 'Ostatnie 7 dni', 'Najbliższe 7 dni', 'Najbliższe 30 dni'))

        selected_timespan_materials_actions_df = db.get_materials_actions(selected_timespan)
        st.dataframe(selected_timespan_materials_actions_df)

        st.divider()

        st.markdown("### Dodaj przyjęcie lub wydanie materiału")

        with st.expander('Rozwiń'):
            with st.form('order'):
                name = st.text_input("Nazwa")
                production_order_id = st.number_input("Numer zlecenia produkcyjnego", min_value=0, step=1)
                action_type = st.selectbox("Rodzaj", ["przyjecie", "wydanie"])
                material = st.text_input("Materiał")
                amount = st.number_input("Ilość", min_value=0, step=1)
                date = st.date_input("Data")
                comment = st.text_area("Uwagi")

                if action_type == 'wydanie':
                    amount = -amount

                submit = st.form_submit_button('Dodaj')
            if submit:
                add_material_action(name, production_order_id, action_type, material, amount, date, comment)
                if action_type == 'przyjecie':
                    st.info('Dodano przyjęcie materiału', icon="ℹ️")
                else:
                    st.info('Dodano wydanie materiału', icon="ℹ️")

        st.divider()

        st.markdown("### Edycja operacji materiałów")

        with st.expander('Rozwiń'):
            original_materials_actions_df = db.get_materials_actions()
            modified_materials_actions_df = st.data_editor(original_materials_actions_df, column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Status",
                    width="medium",
                    options=[
                        "anulowane",
                        "w trakcie",
                        "zakonczone",
                    ],
                ),
                "ID": st.column_config.Column(
                    "ID",
                    help="ID akcji",
                    width="small",
                    disabled=True,
                )
            },
                                                           )
            # Get edited rows and update the DB
            changed_rows_list = utils.get_edited_records(original_materials_actions_df, modified_materials_actions_df)

            if st.button("Zapisz zmiany", key='modify_materials_actions') and len(changed_rows_list) > 0:
                print(changed_rows_list)

                rows_to_update = modified_materials_actions_df.loc[
                    modified_materials_actions_df.index.isin(changed_rows_list)]
                print(rows_to_update)

                # Update the edited rows in the db
                for row in list(rows_to_update.itertuples(index=True, name=None)):
                    db.replace_material_action(row)

                st.info("Zapisano")

        st.divider()
        st.markdown("### Zmiany poziomu zasobu")

        with st.expander('Rozwiń'):
            material_name = st.selectbox("Wybierz materiał", materials_list)
            all_material_actions_df = db.get_all_material_actions(material_name)
            st.dataframe(all_material_actions_df)

            # all_material_actions_df['current_amount'] = all_material_actions_df.loc[::-1, 'Ilość'].cumsum()[::-1]  # Reversed order cumsum

            # fig = px.line(all_material_actions_df, x='Data', y='current_amount',
            #               title=f'Zmiany poziomu materiału {material_name}', text='Nazwa', markers=True, labels={
            #              "current_amount": "Poziom zapasów"
            #          })

            fig = go.Figure(
                go.Waterfall(x=all_material_actions_df.loc[::-1, 'Data'], y=all_material_actions_df.loc[::-1, 'Ilość']))
            # fig.update_traces(textposition="bottom right")

            # Get dates
            # today = pd.to_datetime('today').date()
            # max_future_date = all_material_actions_df['Data'].max()

            # get current values from the db
            material_levels = db.get_material_levels_by_name(material_name)

            fig.add_hline(y=material_levels[0], line_color='green')  # Lower limit
            fig.add_hline(y=material_levels[1], line_color='red')  # Upper limit

            # Add a vertical line at today's date using Plotly Express layout shapes
            # fig.add_vline(x="2018-09-24", line_dash="dash", line_color="red", annotation_text="Today")
            # fig.add_vrect(x0=today, x1=max_future_date, fillcolor="green", opacity=0.15, line_width=0)

            # st.line_chart(all_material_actions_df, x='Data', y='current_amount')
            st.plotly_chart(fig, use_container_width=True)

            with st.form('material_levels'):
                st.write('Zmiana progów decyzyjnych')
                if material_levels is None:
                    lower_limit = st.number_input(f"Poziom zamawiania (obecnie: nie ustawiono)")
                    upper_limit = st.number_input(f"Poziom maksymalny (obecnie: nie ustawiono)")
                    average_delivery_time = st.number_input(f"Średni czas dostawy (obecnie: nie ustawiono)")
                else:
                    lower_limit = st.number_input(f"Poziom zamawiania (obecnie: {material_levels[0]})",
                                                  value=material_levels[0])
                    upper_limit = st.number_input(f"Poziom maksymalny (obecnie: {material_levels[1]})",
                                                  value=material_levels[1])
                    average_delivery_time = st.number_input(f"Średni czas dostawy (obecnie: {material_levels[2]})",
                                                            value=material_levels[2])

                submit = st.form_submit_button('Aktualizuj')
            if submit:
                change_or_add_material_action(material_name, lower_limit, upper_limit, average_delivery_time)
                st.info('Zaktualizowano', icon="ℹ️")

            # Calculate final value, and show notification if its below the lower level
            df = all_material_actions_df.sort_values(by='Data')
            df['current_level'] = df["Ilość"].cumsum()
            df['below_lower_level'] = df['current_level'] <= lower_limit

            # Get the nearest 'below_lower_level' date
            below_lower_level_dates = df.loc[df['below_lower_level'] == True, 'Data']

            if below_lower_level_dates.shape[0] > 0:
                first_below_lower_level_date = below_lower_level_dates.iloc[0]
                st.warning(f"Sugerowana data złożenia zamówienia na dostawę materiału przed: {first_below_lower_level_date - datetime.timedelta(days=average_delivery_time)}")
else:
    st.warning("Proszę się zalogować!")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
