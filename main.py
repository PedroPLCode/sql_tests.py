import sqlite3
from sqlite3 import Error

def create_connection_with_db(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except sqlite3.Error as error:
       print(error)
   return conn


def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as error:
       print(error)
       
       
def add_car_to_db(conn, car):
   """
   Create a new car into the cars table
   :param conn:
   :param car:
   :return: car_id
   """
   sql = '''INSERT INTO cars(name, brand, year, reg_plates)
             VALUES(?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, car)
   conn.commit()
   return cur.lastrowid


def add_driver_to_db(conn, driver):
   """
   Create a new driver into the drivers table
   :param conn:
   :param drivers:
   :return: driver_id
   """
   sql = '''INSERT INTO drivers(car_id, name, experience, status, licence_expiry_date)
             VALUES(?,?,?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, driver)
   conn.commit()
   return cur.lastrowid


def select_all(conn, table):
   """
   Query all rows in the table
   :param conn: the Connection object
   :return:
   """
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows


def select_where(conn, table, **query):
   """
   Query tasks from table with data from **query dict
   :param conn: the Connection object
   :param table: table name
   :param query: dict of attributes and values
   :return:
   """
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows


def update(conn, table, id, **kwargs):
   """
   update car or driver
   :param conn:
   :param table: table name
   :param id: row id
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )
   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)
       
       
def delete(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs) 
    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")
    
    
def delete_all(conn, table):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")


if __name__ == "__main__":

    create_cars_sql_db = """
    -- cars table
    CREATE TABLE IF NOT EXISTS cars (
        id integer PRIMARY KEY,
        name text NOT NULL,
        brand text NOT NULL,
        year text NOT NULL,
        reg_plates text NOT NULL
    );
    """

    create_drivers_sql_db = """
    -- drivers table
    CREATE TABLE IF NOT EXISTS drivers (
        id integer PRIMARY KEY,
        car_id integer NOT NULL,
        name VARCHAR(250) NOT NULL,
        experience TEXT,
        status text NOT NULL,
        licence_expiry_date text NOT NULL,        
        FOREIGN KEY (car_id) REFERENCES cars (id)
    );
    """
    
    cars = [
        ("Fiesta", "Ford", "2013", "PO666"),
        ("Corsa", "Opel", "2013", "WW12321"),
        ("Renegade", "Jeep", "2013", "GD123321"),
        ("Logan", "Dacia", "2013", "PO98765"),
    ]

    drivers = [
        ("1", "John Doe", "5 years", "Active", "2027-03-06"),
        ("2", "Jane Smith", "7 years", "Active", "2025-11-12"),
        ("3", "Michael Johnson", "3 years", "Active", "2026-09-22"),
        ("2", "Emily Brown", "6 years", "Active", "2024-08-15"),
        ("4", "David Wilson", "4 years", "Active", "2025-05-18"),
        ("1", "Jessica Martinez", "2 years", "Active", "2027-02-28"),
        ("3", "Christopher Taylor", "8 years", "Active", "2024-10-03"),
        ("2", "Sarah Garcia", "1 year", "Active", "2026-12-09")
    ]

    db_file = "cars_and_drivers_database.db"

    conn = create_connection_with_db(db_file)
    if conn is not None:
        execute_sql(conn, create_cars_sql_db)
        execute_sql(conn, create_drivers_sql_db)
        
        for car in cars:
            add_car_to_db(conn, car)
            
        for driver in drivers:
            add_driver_to_db(conn, driver)

        all_cars = select_all(conn, "cars")
        all_drivers = select_all(conn, "drivers")

        cars_opel = select_where(conn, "cars", brand="Opel")
        drivers_active = select_where(conn, "drivers", status="Active")
        
        update(conn, "cars", 2, reg_plates="XXX32123")
        update(conn, "drivers", 3, status="Suspended")
        
        delete(conn, "cars", id=4)
        delete(conn, "drivers", id=6)
        
        delete_all(conn, "cars")
        delete_all(conn, "drivers")

        conn.close()