import mysql.connector as ms

# Establish initial connection to create the database if it doesn't exist
try:
    connection = ms.connect(host="localhost", user="root", password="iamsql")
    if connection.is_connected():
        print("Connection successful")
    cur = connection.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS work")
except ms.Error as err:
    print(f"Error: {err}")
else:
    # Connect to the database "work"
    connection = ms.connect(host="localhost", user="root", password="iamsql", port=3308, database="work")
    cur = connection.cursor()
    
    # Create table 'users' if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
    )
    """)
    connection.commit()
    
    # CRUD functions
    def create_record(connection, name, age):
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (name, age) VALUES (%s, %s)"
            cursor.execute(query, (name, age))
            connection.commit()
            print("Record inserted successfully")
        except ms.Error as err:
            print(f"Error: {err}")

    def read_records(connection):
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                for row in data:
                    print(row)
                return data
            else:
                print("No records found.")
                return []
        except ms.Error as err:
            print(f"Error: {err}")
            return []

    def update_record(connection, user_id, name, age):
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET name = %s, age = %s WHERE id = %s"
            cursor.execute(query, (name, age, user_id))
            connection.commit()
            if cursor.rowcount > 0:
                print("Record updated successfully")
            else:
                print("No record found with that ID.")
        except ms.Error as err:
            print(f"Error: {err}")

    def delete_record(connection, user_id):
        try:
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            if cursor.rowcount > 0:
                print("Record deleted successfully")
            else:
                print("No record found with that ID.")
        except ms.Error as err:
            print(f"Error: {err}")

    # Main loop for CRUD operations
    print("WELCOME TO CRUD OPERATIONS!!!")
    print("Please enter your choice:")
    print("1. CREATE")
    print("2. READ")
    print("3. UPDATE")
    print("4. DELETE")
    
    continue_flag = True
    while continue_flag:
        try:
            ch = int(input("Enter your choice (1-4): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        if ch == 1:
            n = input("Enter name: ")
            try:
                a = int(input("Enter age: "))
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue
            create_record(connection, n, a)

        elif ch == 2:
            read_records(connection)

        elif ch == 3:
            try:
                u = int(input("Enter userid: "))
            except ValueError:
                print("Invalid userid. Please enter a number.")
                continue
            n = input("Enter new name: ")
            try:
                a = int(input("Enter new age: "))
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue
            update_record(connection, u, n, a)

        elif ch == 4:
            try:
                u = int(input("Enter userid: "))
            except ValueError:
                print("Invalid userid. Please enter a number.")
                continue
            delete_record(connection, u)

        else:
            print("Enter a choice between 1 and 4 only")
        
        # Ask the user if they wish to continue
        cont = input("Do you want to continue? (Press 1 to continue, any other key to exit): ")
        if cont != "1":
            continue_flag = False

    connection.close()
    print("Database connection closed.")
