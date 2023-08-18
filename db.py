"""
AWS RDS connection for all the pages
"""
import mysql.connector
import pandas
import pandas as pd
import os


# Establish a connection to the database
def create_connection():
    connection = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    return connection


def insert_user(created_at, created_by_id, name, surname, email, username, password_hash, role):
    print("Adding a new user...")
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (created_at, created_by_id, name, surname, email, username, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, name, surname, email, username, password_hash, role))
    connection.commit()

    cursor.close()
    connection.close()


def get_users() -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT users.id, users.created_at, CONCAT(users2.name, ' ' ,users2.surname), users.name, users.surname, users.email, users.role, users.username, users.password_hash
    FROM users
    JOIN users AS users2 ON users.created_by_id = users2.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Imię', 'Nazwisko', 'Email', 'Rodzaj', 'Nazwa Użytkownika', 'Hash'])
    df = df.set_index('ID')
    return df

def get_user_by_id(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}';"
    cursor.execute(query)
    row = cursor.fetchall()

    cursor.close()
    connection.close()

    return row


def get_user_role_by_username(username) -> str or None:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT role FROM users WHERE username = '{username}';"
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is not None:
        return str(row[0])
    else:
        return None


def get_number_of_users():
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM users;"
    cursor.execute(query)
    number_of_users = cursor.fetchone()

    cursor.close()
    connection.close()

    return int(number_of_users[0])


# Trade orders
def insert_trade_order(created_at, created_by_id, status, name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost, price):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO trade_orders (created_at, created_by_id, status, name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, status, name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost, price))
    connection.commit()

    cursor.close()
    connection.close()


def replace_trade_order(trade_order_data):
    connection = create_connection()
    cursor = connection.cursor()
    query = "REPLACE INTO trade_orders (id, created_at, created_by_id, status, name, order_number, order_type, client, material, number_ordered, number_to_make, deadline, comment, cost, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, trade_order_data)
    connection.commit()

    cursor.close()
    connection.close()


def get_trade_orders():
    connection = create_connection()
    cursor = connection.cursor()
    # query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.status, t.name, t.order_number, t.order_type, t.client, t.material, t.number_ordered, t.number_to_make, t.deadline, t. comment, t.cost, t.price
    # FROM trade_orders AS t
    # JOIN users ON users.created_by_id = users.id
    # ORDER BY t.id DESC
    # """
    query = """SELECT * FROM trade_orders
    ORDER BY id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Status', 'Nazwa', 'Numer', 'Rodzaj', 'Kontrahent', 'Meteriał', 'Liczba zlecona', 'Liczba do uruchomienia', 'Planowana data dostarczenia', 'Uwagi', 'Techniczny koszt wytworzenia', 'Wartość'])
    df = df.set_index('ID')
    # df['Rodzaj'] = df['Rodzaj'].astype("category")
    return df


def get_awaiting_trade_orders_number():
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT COUNT(*)
    FROM trade_orders
    WHERE status = 'Oczekujące';
    """
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return int(row[0])


def get_trade_orders_number_next_7d():
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT COUNT(*)
    FROM trade_orders
    WHERE deadline BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY);
    """
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return int(row[0])


def insert_holiday(created_at, created_by_id, date, name):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO holidays (created_at, created_by_id, date, name) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, date, name))
    cursor.close()
    connection.close()


def get_holidays():
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT date, name FROM holidays"""
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['Data', 'Nazwa'])
    # df = df.set_index('ID')

    return df


def update_holidays(created_at, created_by_id, holidays_df):
    connection = create_connection()
    cursor = connection.cursor()

    query1 = """DELETE FROM holidays;
    ALTER TABLE holidays AUTO_INCREMENT = 1;"""
    cursor.execute(query1)
    # rows = cursor.fetchall()

    cursor.close()
    connection.close()

    connection = create_connection()
    cursor = connection.cursor()

    for row in list(holidays_df.itertuples(index=False, name=None)):
        query2 = "INSERT INTO holidays (created_at, created_by_id, date, name) VALUES (%s, %s, %s, %s)"

        data = (created_by_id,) + tuple(row)
        data = (created_at,) + data

        print(data)
        cursor.execute(query2, data)

        connection.commit()


def insert_material_action(created_at, created_by, name, production_order_id, action_type, material, amount, date, comment):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO materials_actions (created_at, created_by_id, name, production_order_id, action_type, material, amount, date, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by, name, production_order_id, action_type, material, amount, date, comment))
    connection.commit()

    cursor.close()
    connection.close()


def get_nearest_material_in():
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT DATEDIFF(date, CURDATE()) AS days_to_date
    FROM materials_actions
    WHERE action_type = 'przyjecie'
    AND status != 'anulowane'
    AND DATEDIFF(date, CURDATE()) >= 0
    ORDER BY DATEDIFF(date, CURDATE())
    LIMIT 1;"""
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is not None:
        return row[0]
    else:
        return 0


def get_materials_list() -> list:
    """
    Get the unique values from the materials actions table
    :return: List of materials in the materials_actions table
    """
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT DISTINCT material
    FROM materials_actions
    ORDER BY material;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [row[0] for row in rows]


def get_materials_actions(selected_timespan=False) -> pandas.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()

    today = pd.to_datetime('today').date()

    if selected_timespan == 'Ostatnie 30 dni':
        query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
        FROM materials_actions AS t
        JOIN users ON users.created_by_id = users.id
        WHERE t.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND t.date <= CURDATE()
        ORDER BY t.date DESC
        """

    elif selected_timespan == 'Ostatnie 7 dni':
        query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
        FROM materials_actions AS t
        JOIN users ON users.created_by_id = users.id
        WHERE t.date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND t.date <= CURDATE()
        ORDER BY t.date DESC
        """
    elif selected_timespan == 'Najbliższe 7 dni':
        query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
        FROM materials_actions AS t
        JOIN users ON users.created_by_id = users.id
        WHERE t.date >= DATE_ADD(CURDATE(), INTERVAL 7 DAY) AND t.date >= CURDATE()
        ORDER BY t.date DESC
        """
    elif selected_timespan == 'Najbliższe 30 dni':
        query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
        FROM materials_actions AS t
        JOIN users ON users.created_by_id = users.id
        WHERE t.date >= DATE_ADD(CURDATE(), INTERVAL 30 DAY) AND t.date >= CURDATE()
        ORDER BY t.date DESC
        """
    else:
        query = """SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
        FROM materials_actions AS t
        JOIN users ON users.created_by_id = users.id
        ORDER BY t.id DESC
        LIMIT 100
        """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Nazwa', 'Przyporządkowane zlecenie produkcyjne', 'Rodzaj', 'Meteriał', 'Ilość', 'Data', 'Status', 'Uwagi'])
    df = df.set_index('ID')
    # df['Rodzaj'] = df['Rodzaj'].astype("category")
    return df


def get_all_material_actions(material_name):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT t.id, t.created_at, CONCAT(users.name, ' ' ,users.surname), t.name, t.production_order_id, t.action_type, t.material, t.amount, t.date, t.status, t.comment
    FROM materials_actions AS t
    JOIN users ON users.created_by_id = users.id
    WHERE t.material = '{material_name}' AND t.status <> 'anulowane' AND t.status IS NOT NULL
    ORDER BY t.date DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Nazwa', 'Przyporządkowane zlecenie produkcyjne', 'Rodzaj', 'Meteriał', 'Ilość', 'Data', 'Status', 'Uwagi'])
    df = df.set_index('ID')
    # df['Rodzaj'] = df['Rodzaj'].astype("category")
    return df


def replace_material_action(material_action_data):
    connection = create_connection()
    cursor = connection.cursor()
    query = "REPLACE INTO materials_actions (created_at, created_by_id, name, production_order_id, action_type, material, amount, date, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, material_action_data)
    connection.commit()

    cursor.close()
    connection.close()


def get_material_levels_by_name(material_name) -> str or None:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"SELECT lower_limit, upper_limit, average_delivery_time FROM materials_levels WHERE material = '{material_name}';"
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is not None:
        return row
    else:
        return 0,0,0


def replace_material_levels(created_at, created_by_id, material_name, lower_limit, upper_limit, average_delivery_time):
    connection = create_connection()
    cursor = connection.cursor()
    query = """INSERT INTO materials_levels (created_at, created_by_id, material, lower_limit, upper_limit, average_delivery_time)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    lower_limit = VALUES(lower_limit),
    upper_limit = VALUES(upper_limit),
    average_delivery_time = VALUES(average_delivery_time),
    created_at = VALUES(created_at),
    created_by_id = VALUES(created_by_id);
    """
    cursor.execute(query, (created_at, created_by_id, material_name, lower_limit, upper_limit, average_delivery_time))
    connection.commit()

    cursor.close()
    connection.close()


def get_materials_below_lower_limit():
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT subq.material, subq.total_amount
    FROM (
        SELECT ml.material, SUM(ma.amount) AS total_amount
        FROM materials_levels AS ml
        JOIN materials_actions AS ma ON ml.material = ma.material
        GROUP BY ml.material
    ) AS subq
    JOIN materials_levels AS ml ON subq.material = ml.material
    WHERE subq.total_amount < ml.lower_limit;"""
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    df = pd.DataFrame(rows, columns=['material', 'number'])
    materials_list = df['material'].unique()
    # df['Rodzaj'] = df['Rodzaj'].astype("category")
    return materials_list


def insert_employee(created_at, created_by, worker_name, worker_surname, worker_work_cost_hour, worker_type):
    print("Adding a new employee...")
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO employees (created_at, created_by_id, name, surname, work_cost_hour, type) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by, worker_name, worker_surname, worker_work_cost_hour, worker_type))
    connection.commit()

    cursor.close()
    connection.close()


def get_employees() -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM employees
    ORDER BY id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Imię', 'Nazwisko', 'Godzinny koszt pracy', 'Rodzaj'])
    df = df.set_index('ID')

    return df


def update_employees(employees_df):
    connection = create_connection()
    cursor = connection.cursor()

    query1 = """DELETE FROM employees;
    ALTER TABLE holidays AUTO_INCREMENT = 1;"""
    cursor.execute(query1)
    # rows = cursor.fetchall()

    cursor.close()
    connection.close()

    connection = create_connection()
    cursor = connection.cursor()

    for row in list(employees_df.itertuples(index=False, name=None)):
        query2 = "INSERT INTO employees (created_at, created_by_id, name, surname, work_cost_hour, type) VALUES (%s, %s, %s, %s, %s, %s)"

        # data = (created_by_id,) + tuple(row)
        # data = (created_at,) + data

        # print(data)
        cursor.execute(query2, tuple(row))

        connection.commit()


def get_number_of_employees() -> int:
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM employees;"
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row[0]


def get_number_of_absent_employees(date, shift=1) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT COUNT(*) FROM attendance
    WHERE present = 0 AND date = {date} AND shift = {shift};"""
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row[0]


def get_attendance_by_date(date):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT * FROM attendance
    WHERE date = {date}
    ORDER BY shift, present DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Data', 'Zmiana', 'Pracownik', 'Obecność', 'Komentarz'])
    df = df.set_index('ID')

    return df


def add_record_to_attendance_list(created_at, created_by, date, shift, employee, present, comment):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO attendance (created_at, created_by_id, date, shift, employee_id, present, comment) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by, date, shift, employee, present, comment))
    connection.commit()

    cursor.close()
    connection.close()


def get_tool_by_number(tool_number) -> int:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT name, specification FROM tools
    WHERE number = {tool_number};"""
    print(query)
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row


def insert_tool(created_at, created_by, name, number, specification):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO tools (created_at, created_by_id, name, number, specification) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by, name, number, specification))
    connection.commit()

    cursor.close()
    connection.close()


def get_tools() -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT tools.id, tools.created_at, CONCAT(users.name, ' ' ,users.surname), tools.name, tools.number, tools.specification FROM tools
    JOIN users ON users.created_by_id = users.id
    ORDER BY tools.id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Nazwa', 'Numer', 'Opis'])
    df = df.set_index('ID')

    return df


def insert_machine(created_at, created_by_id, name, type, work_cost_hour):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO machines (created_at, created_by_id, name, type, work_cost_hour) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, name, type, work_cost_hour))
    connection.commit()

    cursor.close()
    connection.close()


def get_machines() -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT machines.id, machines.created_at, CONCAT(users.name, ' ' ,users.surname), machines.name, machines.type, machines.work_cost_hour FROM machines
    JOIN users ON users.created_by_id = users.id
    ORDER BY machines.id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Nazwa', 'Rodzaj', 'Godzinny koszt pracy'])
    df = df.set_index('ID')

    return df


def get_number_of_machines() -> int:
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM machines;"
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row[0]


def insert_production_order(created_at, created_by_id, name, order_number, trade_order_id, number, start, deadline, progress, material, status, comment):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO production_orders (created_at, created_by_id, name, order_number, trade_order_id, number, start, deadline, progress, material, status, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, name, order_number, trade_order_id, number, start, deadline, progress, material, status, comment))
    connection.commit()

    cursor.close()
    connection.close()


def get_active_production_orders_number():
    connection = create_connection()
    cursor = connection.cursor()
    query = """SELECT COUNT(*)
    FROM production_orders
    WHERE progress < 100;
    """
    cursor.execute(query)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return int(row[0])


def get_production_orders(non_finished_only=False) -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    if non_finished_only:
        query = """SELECT production_orders.id, production_orders.created_at, CONCAT(users.name, ' ' ,users.surname), production_orders.name, production_orders.order_number, production_orders.trade_order_id, production_orders.number, production_orders.start, production_orders.deadline, production_orders.progress, production_orders.material, production_orders.status, production_orders.comment FROM production_orders
        JOIN users ON users.created_by_id = users.id
        WHERE production_orders.status != 'zakończone' AND production_orders.progress < 100
        ORDER BY production_orders.id DESC
        """
    else:
        query = """SELECT production_orders.id, production_orders.created_at, CONCAT(users.name, ' ' ,users.surname), production_orders.name, production_orders.order_number, production_orders.trade_order_id, production_orders.number, production_orders.start, production_orders.deadline, production_orders.progress, production_orders.material, production_orders.status, production_orders.comment FROM production_orders
        JOIN users ON users.created_by_id = users.id
        ORDER BY production_orders.id DESC
        """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Nazwa', 'Numer', 'Zlecenie Handlowe', 'Liczba', 'Start', 'Koniec', 'Poziom wykon.', 'Materiał', 'Status', 'Uwagi'])
    df = df.set_index('ID')

    return df


def update_production_order(selected_production_order, deadline, progress, status):
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""UPDATE production_orders
    SET
      deadline = '{deadline}',
      progress = {progress},
      status = '{status}'
    WHERE
        order_number = {selected_production_order};"""
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def insert_machine_action(created_at, created_by_id, production_order_number, state, start_date, finish_date, machine_id):
    print(created_at, created_by_id, production_order_number, state, start_date, finish_date)
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO machines_actions (created_at, created_by_id, production_order_number, state, start_date, finish_date, machine_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, int(production_order_number), int(state), start_date, finish_date, machine_id))
    connection.commit()

    cursor.close()
    connection.close()


def get_machines_actions_between_dates(machine_id, start, finish) -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT *
    FROM machines_actions
    WHERE machine_id = {machine_id}
    AND start_date >= '{start}'
    AND finish_date <= '{finish}';"""
    print(query)
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Zlecenie produkcyjne', 'Status', 'Początek', 'Koniec', 'ID maszyny'])
    df = df.set_index('ID')
    df['Zlecenie produkcyjne'] = df['Zlecenie produkcyjne'].astype(str)

    # change the time
    df['Początek'] = pd.to_datetime(df['Początek'])
    df['Początek'] = df['Początek'].apply(lambda x: x.replace(hour=0, minute=1))

    df['Koniec'] = pd.to_datetime(df['Koniec'])

    df['Koniec'] = df['Koniec'].apply(lambda x: x.replace(hour=23, minute=59))

    return df


def get_employees_actions_between_dates(employee_id, start, finish) -> pd.DataFrame:
    connection = create_connection()
    cursor = connection.cursor()
    query = f"""SELECT *
    FROM employees_actions
    WHERE employee_id = {employee_id}
    AND start_date >= '{start}'
    AND finish_date <= '{finish}';"""
    print(query)
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    # for row in rows:
    #     print(row)

    df = pd.DataFrame(rows, columns=['ID', 'Utworzono', 'Utworzone przez', 'Zlecenie produkcyjne', 'Status', 'Początek', 'Koniec', 'ID pracownika'])
    df = df.set_index('ID')
    df['Zlecenie produkcyjne'] = df['Zlecenie produkcyjne'].astype(str)

    # change the time
    df['Początek'] = pd.to_datetime(df['Początek'])
    df['Początek'] = df['Początek'].apply(lambda x: x.replace(hour=0, minute=1))

    df['Koniec'] = pd.to_datetime(df['Koniec'])

    df['Koniec'] = df['Koniec'].apply(lambda x: x.replace(hour=23, minute=59))

    return df


def insert_employee_action(created_at, created_by_id, production_order_number, state, start_date, finish_date, employee_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO employees_actions (created_at, created_by_id, production_order_number, state, start_date, finish_date, employee_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (created_at, created_by_id, int(production_order_number), int(state), start_date, finish_date, employee_id))
    connection.commit()

    cursor.close()
    connection.close()


if __name__ == "__main__":
    print(get_tool_by_number('11'))
