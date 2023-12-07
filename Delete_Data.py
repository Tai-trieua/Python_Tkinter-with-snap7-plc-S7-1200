import sqlite3

conn = sqlite3.connect("Database\IoT_Dashboard.db")

cursor = conn.cursor()
sql_Data = """DELETE FROM Data_Table WHERE frequency_out =0.0"""
                                        
cursor.execute(sql_Data)
conn.commit()
cursor.close()