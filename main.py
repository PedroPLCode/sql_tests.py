from utils import *
from settings import *

with create_connection_with_db(db_file) as conn:
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