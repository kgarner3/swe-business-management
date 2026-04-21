import sqlite3
from hash_utilities import HashUtilities

DB_Path = "business.db"

def get_connection():
    """Establishes a connection to the database"""
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the Database """
    conn = get_connection()
    cursor = conn.cursor()

    #This is where the actual SQL is placed to do operations on the DB
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            Customer_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name            TEXT NOT NULL,
            last_name             TEXT NOT NULL,
            email                 TEXT UNIQUE NOT NULL,
            number                TEXT,
            address               TEXT,
            username              TEXT UNIQUE NOT NULL,
            passwordHash          TEXT NOT NULL,
            salt                  TEXT NOT NULL,
            mustChangePassword    INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            Employee_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name            TEXT NOT NULL,
            last_name             TEXT NOT NULL,
            email                 TEXT UNIQUE NOT NULL,
            username              TEXT UNIQUE NOT NULL,
            passwordHash          TEXT NOT NULL,
            salt                  TEXT NOT NULL,
            expenses              REAL NOT NULL DEFAULT 0.0,
            mustChangePassword    INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            Service_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT UNIQUE NOT NULL,
            description   TEXT NOT NULL DEFAULT '',
            cost          REAL NOT NULL DEFAULT 0.0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            Appointment_ID      INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_ID         INTEGER NOT NULL,
            Employee_ID         INTEGER NOT NULL,
            Service_ID          INTEGER NOT NULL,
            date                TEXT NOT NULL,
            description         TEXT NOT NULL DEFAULT '',
            cost                REAL NOT NULL DEFAULT 0.0,
            additional_expenses REAL NOT NULL DEFAULT 0.0,
            status              TEXT NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID),
            FOREIGN KEY (Employee_ID) REFERENCES employees(Employee_ID),
            FOREIGN KEY (Service_ID)  REFERENCES services(Service_ID),
            UNIQUE (Customer_ID, date),
            UNIQUE (Employee_ID, date)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            Expense_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
            Employee_ID   INTEGER NOT NULL,
            amount        REAL NOT NULL,
            date          TEXT NOT NULL,
            description   TEXT NOT NULL,
            FOREIGN KEY (Employee_ID) REFERENCES employees(Employee_ID)
        )
    ''')

    conn.commit()   #saves
    conn.close()    #closes connection to the database

def seed_customers():
    """Default customers"""
    conn = get_connection()
    cursor = conn.cursor()

    customers = [
        ("John", "Doe", "john@example.com", "555-111-1111", "123 Main St", "jdoe"),
        ("Jane", "Smith", "jane@example.com", "555-222-2222", "456 Oak Ave", "jsmith"),
        ("Mike", "Brown", "mike@example.com", "555-333-3333", "789 Pine Rd", "mbrown"),
        ("Emily", "Davis", "emily@example.com", "555-444-4444", "321 Elm St", "edavis"),
        ("Chris", "Wilson", "chris@example.com", "555-555-5555", "654 Maple Dr", "cwilson"),
        ("Sarah", "Miller", "sarah@example.com", "555-666-6666", "987 Cedar Ln", "smiller"),
        ("David", "Taylor", "david@example.com", "555-777-7777", "159 Birch St", "dtaylor"),
        ("Laura", "Anderson", "laura@example.com", "555-888-8888", "753 Walnut Ave", "landerson"),
        ("James", "Thomas", "james@example.com", "555-999-9999", "852 Spruce Dr", "jthomas"),
        ("Olivia", "Jackson", "olivia@example.com", "555-000-0000", "147 Aspen Ct", "ojackson")
    ]

    for first, last, email, phone, address, username in customers:
        temp_password = "temp123"
        passwordHash, salt = HashUtilities.hash_password(temp_password)

        try:
            cursor.execute('''
                INSERT INTO customers 
                (first_name, last_name, email, number, address, username, passwordHash, salt, mustChangePassword)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first, last, email, phone, address, username, passwordHash, salt, 1))
        except:
            pass  # ignore duplicates

    conn.commit()   #saves
    conn.close()    #closes connection to the database


def seed_employees():
    """Default employees"""
    conn = get_connection()
    cursor = conn.cursor()

    employees = [
        ("Admin", "User", "admin@test.com", "admin"),
        ("Katie", "Garner", "kgarner3@students.towson.edu", "kgarner3"),
        ("Matheus", "Mendez", "mmendes3@students.towson.edu", "mmendes3"),
        ("Gabriel", "Walsh", "gwalsh6@students.towson.edu", "gwalsh6"),
        ("Natnael", "Yonas", "nyonas3@students.towson.edu", "nyonas3"),
        ("Javier", "Velasquez", "jvelasq3@students.towson.edu", "jvelasq3"),
    ]

    for first, last, email, username in employees:
        temp_password = "temp123"
        passwordHash, salt = HashUtilities.hash_password(temp_password)

        try:
            cursor.execute('''
                INSERT INTO employees
                (first_name, last_name, email, username, passwordHash, salt, expenses, mustChangePassword)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first, last, email, username, passwordHash, salt, 0.0, 1))
        except:
            pass  # ignore duplicates if rerun

    conn.commit()   #saves
    conn.close()    #closes connection to the database

def seed_services():
    """Default services"""
    conn = get_connection()
    cursor = conn.cursor()

    services = [
        ("AC Installation",
        "Full installation of a new central air conditioning unit, including ductwork connection and system testing.",
        2400.00),
        ("AC Repair",
        "Diagnosis and repair of a malfunctioning air conditioning system, including parts and labor.",
        320.00),
        ("AC Tune-Up",
        "Seasonal maintenance inspection, coil cleaning, refrigerant check, and filter replacement.",
        120.00),
        ("Furnace Installation",
        "Installation of a new gas or electric furnace with thermostat setup and safety inspection.",
        2100.00),
        ("Furnace Repair",
        "Diagnosis and repair of furnace issues including igniter, blower motor, or heat exchanger problems.",
        290.00),
        ("Furnace Tune-Up",
        "Annual furnace inspection, burner cleaning, flue check, and filter replacement.",
        110.00),
        ("Heat Pump Installation",
        "Installation of a new heat pump system for year-round heating and cooling.",
        3200.00),
        ("Heat Pump Repair",
        "Diagnosis and repair of heat pump electrical, refrigerant, or mechanical issues.",
        350.00),
        ("Ductwork Inspection & Sealing",
        "Full duct system inspection with sealing of leaks to improve airflow efficiency.",
        480.00),
        ("Ductwork Replacement",
        "Complete replacement of old or damaged ductwork throughout the home.",
        1800.00),
        ("Indoor Air Quality Assessment",
        "Testing and evaluation of indoor air quality including humidity, VOCs, and particulate levels.",
        200.00),
        ("Air Purifier Installation",
        "Installation of a whole-home air purification system integrated into existing HVAC.",
        650.00),
        ("Thermostat Installation",
        "Installation and programming of a new smart or standard thermostat.",
        180.00),
        ("Emergency HVAC Service",
        "Priority same-day response for HVAC system failures outside of normal business hours.",
        500.00),
        ("HVAC System Replacement",
        "Full replacement of an aging HVAC system including removal of old equipment and installation of new unit.",
        5500.00),
    ]

    for name, description, cost in services:
        try:
            cursor.execute('''
                INSERT INTO services (name, description, cost)
                VALUES (?, ?, ?)
            ''', (name, description, cost))
        except:
            pass  # ignore duplicates if rerun

    conn.commit()
    conn.close()


def seed_appointments():
    """
    Seeds demo appointments with unique customer/employee/date combinations.
    - Several completed appointments in the past to trigger win-back for those customers
    - One appointment exactly 7 days from today to trigger reminder email demo
    - One upcoming appointment beyond 7 days
    """
    from datetime import datetime, timedelta

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now()

    def days_ago(n):
        return (today - timedelta(days=n)).strftime("%Y-%m-%d")

    def days_from_now(n):
        return (today + timedelta(days=n)).strftime("%Y-%m-%d")

    def get_customer_id(username):
        cursor.execute('SELECT Customer_ID FROM customers WHERE username = ?', (username,))
        row = cursor.fetchone()
        return row["Customer_ID"] if row else None

    def get_employee_id(username):
        cursor.execute('SELECT Employee_ID FROM employees WHERE username = ?', (username,))
        row = cursor.fetchone()
        return row["Employee_ID"] if row else None

    def get_service_id(name):
        cursor.execute('SELECT Service_ID, cost FROM services WHERE name = ?', (name,))
        row = cursor.fetchone()
        return (row["Service_ID"], row["cost"]) if row else (None, 0.0)

    appointments = [
        ("jdoe",    "kgarner3", "AC Tune-Up",              days_ago(90),    "Completed", 0.00),
        ("jsmith",  "mmendes3", "Furnace Tune-Up",         days_ago(75),    "Completed", 50.00),
        ("mbrown",  "gwalsh6",  "Thermostat Installation", days_ago(60),    "Completed", 0.00),
        ("edavis",  "nyonas3",  "AC Repair",               days_ago(50),    "Completed", 75.00),
        ("cwilson", "jvelasq3", "Furnace Repair",          days_ago(45),    "Completed", 120.00),
        ("smiller", "kgarner3", "AC Installation",         days_from_now(7),  "Scheduled", 0.00),
        ("dtaylor", "mmendes3", "Heat Pump Installation",  days_from_now(30), "Scheduled", 0.00),
    ]

    for cust_username, emp_username, service_name, date, status, add_exp in appointments:
        cust_id = get_customer_id(cust_username)
        emp_id = get_employee_id(emp_username)
        svc_id, cost = get_service_id(service_name)

        if not cust_id or not emp_id or not svc_id:
            continue

        cursor.execute('''
            SELECT 1
            FROM appointments
            WHERE Customer_ID = ?
              AND Employee_ID = ?
              AND Service_ID = ?
              AND date = ?
              AND status = ?
        ''', (cust_id, emp_id, svc_id, date, status))

        already_exists = cursor.fetchone()

        if already_exists:
            continue

        cursor.execute('''
            INSERT INTO appointments
                (Customer_ID, Employee_ID, Service_ID, date, description,
                 cost, additional_expenses, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cust_id, emp_id, svc_id, date, "", cost, add_exp, status))

    conn.commit()
    conn.close()
