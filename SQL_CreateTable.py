import sqlite3

conn = sqlite3.connect('Database\IoT_Dashboard.db')


conn.execute('''CREATE TABLE IF NOT EXISTS Admin_Account
                   (admin_id INTEGER PRIMARY KEY NOT NULL,
                   admin_fullname TEXT ,
                   admin_username TEXT,
                   admin_password TEXT );
                   ''')
                

conn.execute('''CREATE TABLE IF NOT EXISTS Employee_Acount 
                   (employee_id INTEGER PRIMARY KEY NOT NULL,
                   employee_fullname TEXT ,
                   employee_username TEXT,
                   employee_password TEXT );
                   ''')

conn.execute('''CREATE TABLE IF NOT EXISTS Guest_Acount 
                   (guest_id INTEGER PRIMARY KEY NOT NULL,
                   guest_fullname TEXT ,
                   guest_username TEXT,
                   guest_password TEXT );
                   ''')

conn.execute('''CREATE TABLE IF NOT EXISTS Data_Table
                   (data_id INTEGER PRIMARY KEY NOT NULL,
                   frequency_ref REAL, 
                   frequency_out REAL, 
                   voltage_out REAL, 
                   tempurature_1 REAL, 
                   humidity_1  REAL);
                   ''')