import mysql.connector
print("\n \n \n")
print("----------WELCOME TO CRIME RATE ANALYSIS----------")
print("\n")
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "crime_data_db"
}
def insert_data(cursor):
    print("\nYou selected: Enter data into the database.")
    try:
        city = input("Enter City: ")
        crime_desc = input("Enter Crime Description: ")
        victim_age = int(input("Enter Victim Age: "))
        victim_gender = input("Enter Victim Gender (Male/Female): ")
        weapon_used = input("Enter Weapon Used: ")
        case_closed = input("Is the case closed? (Yes/No): ")

        insert_query = """
        INSERT INTO crime_data (City, Crime_Description, Victim_Age, Victim_Gender, Weapon_Used, Case_Closed)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (city, crime_desc, victim_age, victim_gender, weapon_used, case_closed))
        conn.commit()
        print("Data successfully added to the database.\n")
    except ValueError:
        print("Invalid input! Please ensure the data types are correct.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
def fetch_aggregated_data(cursor):
    print("\nYou selected: Fetch data from the database (filtered by gender and aggregated by crime type).")
    try:
        city = input("Enter the City to fetch data: ")
        gender = input("Enter the Victim Gender to filter (Male/Female): ")

        # Query to aggregate data by crime type
        select_query = """
        SELECT 
            Crime_Description,
            COUNT(*) AS crime_count
        FROM crime_data
        WHERE City = %s AND Victim_Gender = %s
        GROUP BY Crime_Description
        ORDER BY crime_count DESC;
        """
        cursor.execute(select_query, (city, gender))
        results = cursor.fetchall()

        if results:
            print(f"\nAggregated crime data for city '{city}' and gender '{gender}':")
            print(f"{'Crime Description':<30}{'Crime Count':<15}")
            print("-" * 45)
            for row in results:
                print(f"{row[0]:<30}{row[1]:<15}")
        else:
            print(f"No data available for city '{city}' and gender '{gender}'.\n")
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
def count_crimes_in_city(cursor):
    print("\nYou selected: Count the number of crimes in a particular city.")
    try:
        city = input("Enter the City to count crimes: ")
        count_query = """
        SELECT 
            COUNT(*) AS total_crimes
        FROM crime_data
        WHERE City = %s;
        """
        cursor.execute(count_query, (city,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            print(f"\nThe total number of crimes reported in city '{city}' is: {result[0]}")
        else:
            print(f"No crime data found for the city '{city}'.\n")
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
def view_data_paginated(cursor, page_size=10):
    print("\nYou selected: View all data (with pagination).")
    try:
        cursor.execute("SELECT COUNT(*) FROM crime_data")
        total_rows = cursor.fetchone()[0]
        print(f"\nTotal rows in the database: {total_rows}")
        
        offset = 0
        while offset < total_rows:
            print(f"\nDisplaying rows {offset + 1} to {min(offset + page_size, total_rows)}:\n")
            cursor.execute(f"SELECT * FROM crime_data LIMIT {page_size} OFFSET {offset}")
            results = cursor.fetchall()
            print(f"{'City':<20}{'Crime Description':<30}{'Age':<5}{'Gender':<10}{'Weapon Used':<20}{'Case Closed':<10}")
            print("-" * 100)
            for row in results:
                print(f"{row[0]:<20}{row[1]:<30}{row[2]:<5}{row[3]:<10}{row[4]:<20}{row[5]:<10}")
            
            offset += page_size
            if offset < total_rows:
                if input("Press Enter to see more or type 'exit' to stop: ").lower() == 'exit':
                    break
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
def generate_report(cursor):
    print("\nYou selected: Generate Reports.")
    try:
        print("\n1. Most Common Crime Types:")
        query1 = """
        SELECT Crime_Description, COUNT(*) AS crime_count
        FROM crime_data
        GROUP BY Crime_Description
        ORDER BY crime_count DESC
        LIMIT 5;
        """
        cursor.execute(query1)
        results = cursor.fetchall()
        print(f"{'Crime Description':<30}{'Count':<10}")
        print("-" * 40)
        for row in results:
            print(f"{row[0]:<30}{row[1]:<10}")
        print("\n2. Cities with the Highest Crime Rates:")
        query2 = """
        SELECT City, COUNT(*) AS total_crimes
        FROM crime_data
        GROUP BY City
        ORDER BY total_crimes DESC
        LIMIT 5;
        """
        cursor.execute(query2)
        results = cursor.fetchall()
        print(f"{'City':<20}{'Total Crimes':<15}")
        print("-" * 35)
        for row in results:
            print(f"{row[0]:<20}{row[1]:<15}")
        print("\n3. Age and Gender Demographics of Victims:")
        query3 = """
        SELECT 
            Victim_Gender,
            CASE
                WHEN Victim_Age BETWEEN 0 AND 10 THEN '0-10'
                WHEN Victim_Age BETWEEN 11 AND 20 THEN '11-20'
                WHEN Victim_Age BETWEEN 21 AND 30 THEN '21-30'
                WHEN Victim_Age BETWEEN 31 AND 40 THEN '31-40'
                WHEN Victim_Age BETWEEN 41 AND 50 THEN '41-50'
                ELSE '51+'
            END AS age_group,
            COUNT(*) AS count
        FROM crime_data
        GROUP BY Victim_Gender, age_group
        ORDER BY Victim_Gender, age_group;
        """
        cursor.execute(query3)
        results = cursor.fetchall()
        print(f"{'Gender':<10}{'Age Group':<10}{'Count':<10}")
        print("-" * 30)
        for row in results:
            print(f"{row[0]:<10}{row[1]:<10}{row[2]:<10}")
    except mysql.connector.Error as err:
        print(f"Error generating report: {err}")
def delete_data(cursor):
    try:
        city = input("Enter the City: ")
        crime_desc = input("Enter the Crime Description: ")
        victim_age = int(input("Enter the Victim Age: "))

        delete_query = """
        DELETE FROM crime_data
        WHERE City = %s AND Crime_Description = %s AND Victim_Age = %s
        """
        cursor.execute(delete_query, (city, crime_desc, victim_age))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"\nThe row matching City: '{city}', Crime Description: '{crime_desc}', and Victim Age: {victim_age} has been deleted.")
        else:
            print("\nNo matching row found to delete.")
    except ValueError:
        print("Invalid input! Please ensure the data types are correct.")
    except mysql.connector.Error as err:
        print(f"Error deleting data: {err}")
def update_data(cursor):
    try:
        city = input("Enter the City of the record to update: ")
        crime_desc = input("Enter the Crime Description of the record to update: ")
        victim_age = int(input("Enter the Victim Age of the record to update: "))

        print("\nEnter the new values (leave blank to keep the current value):")
        new_city = input("New City: ").strip()
        new_crime_desc = input("New Crime Description: ").strip()
        new_victim_age = input("New Victim Age: ").strip()
        new_victim_gender = input("New Victim Gender (Male/Female): ").strip()
        new_weapon_used = input("New Weapon Used: ").strip()
        new_case_closed = input("New Case Closed (Yes/No): ").strip()

        update_query = """
        UPDATE crime_data
        SET 
            City = COALESCE(%s, City),
            Crime_Description = COALESCE(%s, Crime_Description),
            Victim_Age = COALESCE(%s, Victim_Age),
            Victim_Gender = COALESCE(%s, Victim_Gender),
            Weapon_Used = COALESCE(%s, Weapon_Used),
            Case_Closed = COALESCE(%s, Case_Closed)
        WHERE City = %s AND Crime_Description = %s AND Victim_Age = %s
        """
        cursor.execute(
            update_query,
            (
                new_city or None,
                new_crime_desc or None,
                int(new_victim_age) if new_victim_age else None,
                new_victim_gender or None,
                new_weapon_used or None,
                new_case_closed or None,
                city,
                crime_desc,
                victim_age,
            )
        )
        conn.commit()

        if cursor.rowcount > 0:
            print("\nThe record has been successfully updated.")
        else:
            print("\nNo matching record found to update.")
    except ValueError:
        print("Invalid input! Please ensure the data types are correct.")
    except mysql.connector.Error as err:
        print(f"Error updating data: {err}")


# Main program
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to the MySQL database.\n")
    while True:
        print("Select an option:")
        print("1. Enter data into the database")
        print("2. Fetch data (filtered by gender and aggregated by crime type)")
        print("3. Count the number of crimes in a city")
        print("4. View all data (with pagination)")
        print("5. Generate detailed reports")
        print("6. Delete a row from the database")
        print("7. Update a row in the database")
        print("8. Exit")
        choice = input("Enter your choice : ")
        if choice == "1":
            insert_data(cursor)
        elif choice == "2":
            fetch_aggregated_data(cursor)
        elif choice == "3":
            count_crimes_in_city(cursor)
        elif choice== "4":
            view_data_paginated(cursor)
        elif choice == "5":
            generate_report(cursor)
        elif choice == "6":
            delete_data(cursor)
        elif choice == "7":
            update_data(cursor)
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4.\n")
except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
    print("Database connection closed.")
