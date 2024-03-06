db_file = "cars_and_drivers_database.db"

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