import time
import datetime
import db
import streamlit as st
from datetime import timedelta, date



def get_info():
    created_at = datetime.datetime.now()
    created_by_id = 1

    return created_at, created_by_id


def get_edited_records(df_original, df_modified):
    changed_rows = (df_original != df_modified).any(axis=1)
    changed_indexes = df_original.index[changed_rows].tolist()

    return changed_indexes


def create_auth_users_list() -> dict:
    """
    Streamlit Authenticator addon only accepts this format... Better to use a database than a yaml file
    :return:
    """
    users_df = db.get_users()
    # print(users_df)

    # df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Imię', 'Nazwisko', 'Email', 'Rodzaj', 'Nazwa Użytkownika', 'Hash'])
    # df = df.set_index('ID')

    nested_dict = {}

    for index, row in users_df.iterrows():
        user_dict = {
            'email': row['Email'],
            'name': row['Nazwa Użytkownika'],
            'password': row['Hash']
        }

        username = row['Nazwa Użytkownika']  # Assuming usernames are stored as comma-separated strings

        final_user_dict = {username: user_dict}
        # print(final_user_dict)

        nested_dict.update(final_user_dict)

    final_dict = {'usernames': nested_dict}
    return final_dict


def calculate_finish_date(start_date: datetime.date, duration: int,  holidays: list) -> (datetime.date, int, int):
    """
    Calculate finish date - consider weekends and holidays
    :param start_date:
    :param holidays:
    :return: The last date that is assigned to the task (so the date is already filled with the task, if you need to plan a new project - you should assign it to the next day)
    """

    working_days_counter = 0
    free_days_counter = 0

    print(f"Calculating the finish date for {start_date} {duration} {holidays}")
    remaining_days = int(duration)
    current_date = start_date

    while remaining_days > 1:  # 1 because we want only days that are assigned to the task
        current_date += timedelta(days=1)
        # Check if the current day is a weekend
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            free_days_counter += 1
            continue

        # Check if the current day is a holiday
        if current_date in holidays:
            current_date += timedelta(days=1)
            free_days_counter += 1
            continue

        # print(current_date)
        remaining_days -= 1
        working_days_counter += 1

    return current_date, working_days_counter, free_days_counter


@st.cache_data
def get_user_role():
    try:
        return st.session_state["role"]
    except KeyError:
        return None


@st.cache_data
def get_auth_status():
    try:
        return st.session_state["authentication_status"]
    # When starting the app not from the start window all the session states are not loaded
    except KeyError:
        return None


@st.cache_data
def logged():
    if st.session_state["role"] in ['Administrator', 'Dyrektor', 'Specjalista ds. sprzedaży']:
        return True
    else:
        return False


if __name__ == "__main__":
    start_date = "2023-08-10"
    task_duration = 7
    holiday_dates = [
        date(2023, 8, 12),  # Example holiday dates
        date(2023, 8, 16)
    ]
    print(calculate_finish_date(start_date, task_duration, holiday_dates))
