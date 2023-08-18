"""
Create db tables and fill it with records
"""
import mysql.connector
import os

# TODO add NOT NULL
# TODO add foreign keys https://learnsql.com/blog/why-use-foreign-key-in-sql/
# TODO add unsigned
# Establish a connection to the database
def create_connection():
    connection = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        password=os.environ['PASSWORD'],
        database=os.environ['DATABASE']
    )
    return connection


# Create a sample table
def create_trade_orders_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS trade_orders (
  id int PRIMARY KEY AUTO_INCREMENT ,
  created_at timestamp,
  created_by_id int UNSIGNED,
  status varchar(255),
  name varchar(255),
  order_number int UNSIGNED UNIQUE,
  type enum('Zlecenie zewnętrzne', 'Zlecenie wewnętrzne'),
  client varchar(255),
  material varchar(255),
  number_ordered int UNSIGNED,
  number_to_make int UNSIGNED,
  deadline date,
  comment varchar(5000),
  cost float,
  price float
);""")

def create_users_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `created_at` TIMESTAMP,
  `created_by_id` INT UNSIGNED,
  `name` VARCHAR(255),
  `surname` VARCHAR(255),
  `email` VARCHAR(255),
  `username` VARCHAR(255),
  `password_hash` VARCHAR(255),
  `role` VARCHAR(255),
  UNIQUE (username)
);""")


def create_holidays_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE holidays (
    id INT PRIMARY KEY AUTO_INCREMENT,
    created_at TIMESTAMP,
    created_by_id INT UNSIGNED,
    date DATE,
    name VARCHAR(255)
);""")


def create_materials_actions_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `materials_actions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED ,
  `name` varchar(255),
  `production_order_id` int UNSIGNED ,
  `action_type` enum('przyjecie', 'wydanie'),
  `material` varchar(255),
  `amount` float,
  `date` date,
  `comment` varchar(5000),
  `status` enum('anulowane', 'w trakcie', 'zakonczone') DEFAULT 'w trakcie',
   FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`)
    );""")


def create_materials_levels_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `materials_levels` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `material` varchar(255),
  `lower_limit` float,
  `upper_limit` float,
  `average_delivery_time` int,
  FOREIGN KEY (`created_by_id`) REFERENCES `users`(`id`),
  UNIQUE (material)
);""")


def create_employees_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `employees` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `name` varchar(255),
  `surname` varchar(255),
  `work_cost_hour` float,
  `type` varchar(255)
);""")


def create_machines_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `machines` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `name` varchar(255),
  `type` varchar(255),
  `work_cost_hour` float
);""")


def create_attendance_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `attendance` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `date` date NOT NULL,
  `shift` int DEFAULT 1,
  `employee_id` int NOT NULL,
  `present` bool,
  `comment` varchar(255),
  UNIQUE KEY unique_attendance (employee_id, date, shift)
);""")


def create_tools_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `tools` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `name` varchar(255),
  `number` varchar(255) UNIQUE,
  `specification` varchar(255)
);""")


def create_production_orders_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `production_orders` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `name` varchar(255),
  `order_number` int UNIQUE,
  `trade_order_id` int,
  `number` int ,
  `start` date,
  `deadline` date COMMENT 'default 0',
  `progress` int,
  `material` varchar(255),
  `status` varchar(255),
  `comment` varchar(255)
);""")


def create_machines_actions_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `machines_actions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `production_order_number` int,
  `state` int UNSIGNED,
  `start_date` date,
  `finish_date` date,
  `machine_id` int
);""")


def create_employees_actions_table(connection):
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE `employees_actions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `created_by_id` int UNSIGNED,
  `production_order_number` int,
  `state` int UNSIGNED,
  `start_date` date,
  `finish_date` date,
  `employee_id` int
);""")


connection = create_connection()
# create_table(connection)
#
# insert_record(connection, "John Doe", 30)
# insert_record(connection, "Jane Smith", 28)

# select_records(connection)
# create_trade_orders_table(connection)
# create_holidays_table(connection)
# create_materials_levels_table(connection)
# create_machines_table(connection)
# create_employees_table(connection)
# create_attendance_table(connection)
# create_tools_table(connection)
# create_production_orders_table(connection)
# create_machines_actions_table(connection)
# create_employees_actions_table(connection)
