import mysql.connector
import csv
db_config = {
    "host": "localhost",  
    "user": "root", 
    "password": "123456"  
}
database_name = "crime_data_db"
table_name = "crime_data"
csv_file_path = "C:/Users/Acer/Desktop/crime_dataset_india.csv"
try:
    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()
    print("Connected to MySQL server.")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()
try:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database {database_name} created or already exists.")
    conn.database = database_name  
except mysql.connector.Error as err:
    print(f"Error creating database: {err}")
    conn.close()
    exit()
table_creation_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    City VARCHAR(255),
    Crime_Description VARCHAR(255),
    Victim_Age INT,
    Victim_Gender VARCHAR(10),
    Weapon_Used VARCHAR(100),
    Case_Closed VARCHAR(20)
);
"""
try:
    cursor.execute(table_creation_query)
    print(f"Table {table_name} is ready.")
except mysql.connector.Error as err:
    print(f"Error creating table: {err}")
    conn.close()
    exit()
try:
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  
        insert_query = f"INSERT INTO {table_name} (City,Crime_Description, Victim_Age,Victim_Gender,Weapon_Used,Case_Closed) VALUES (%s, %s, %s,%s,%s,%s)"
        for row in csv_reader:
            cursor.execute(insert_query, row)
    conn.commit()
    print("Data successfully inserted into the database.")
except FileNotFoundError:
    print("CSV file not found. Please check the file path.")
except mysql.connector.Error as err:
    print(f"Error inserting data: {err}")
finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
