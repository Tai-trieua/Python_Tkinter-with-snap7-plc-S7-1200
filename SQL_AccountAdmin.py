import sqlite3

conn = sqlite3.connect("Database\IoT_Dashboard.db")

cursor = conn.cursor()
sql_adminAccount = """INSERT INTO Admin_Account (admin_id, admin_fullname,admin_username, admin_password) VALUES
                                        (2,'Super User', 'Admin','admin')"""
                                        
cursor.execute(sql_adminAccount)
conn.commit()
cursor.close()