import mysql.connector
from mysql.connector import Error
import getpass

# Establish database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         
            password='',         
            database='train_database'      
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Update Database Schema
def update_user_table_schema():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    try:
        # Add new columns if they don't already exist
        query = """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS nid VARCHAR(50),
        ADD COLUMN IF NOT EXISTS birth_certificate VARCHAR(50),
        ADD COLUMN IF NOT EXISTS email VARCHAR(100),
        ADD COLUMN IF NOT EXISTS mobile_number VARCHAR(15)
        """
        cursor.execute(query)
        db.commit()
        print("Database schema updated successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

# Admin Login
def admin_login():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return False

    cursor = db.cursor()
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")  
    try:
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            print("Admin login successful!")
            return True
        else:
            print("Invalid admin credentials!")
            return False
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

# User Login
def user_login():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return None

    cursor = db.cursor()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    try:
        query = "SELECT id FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            print("User login successful!")
            return result[0]  # Return user ID
        else:
            print("Invalid user credentials!")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        db.close()

# User Registration
def user_register():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return None

    cursor = db.cursor()
    username = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")
    nid = input("Enter your National ID (NID): ")
    birth_certificate = input("Enter your Birth Certificate Number: ")
    email = input("Enter your Email Address: ")
    mobile_number = input("Enter your Mobile Number: ")

    try:
        query = """
            INSERT INTO users (username, password, nid, birth_certificate, email, mobile_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, password, nid, birth_certificate, email, mobile_number))
        db.commit()
        print("Registration successful! You can now log in.")
        return cursor.lastrowid  # Return new user ID
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        db.close()

# Admin Section
def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Train")
        print("2. View Trains")
        print("3. Add Food Item")
        print("4. View Food Items")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_train()
        elif choice == "2":
            view_trains()
        elif choice == "3":
            add_food_item()
        elif choice == "4":
            view_food_items()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

def add_train():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    train_name = input("Enter train name: ")
    source = input("Enter source: ")
    destination = input("Enter destination: ")
    departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS): ")
    arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM:SS): ")

    try:
        query = "INSERT INTO trains (train_name, source, destination, departure_time, arrival_time) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (train_name, source, destination, departure_time, arrival_time))
        db.commit()
        print("Train added successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

def add_food_item():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    item_name = input("Enter food item name: ")
    price = float(input("Enter price: "))

    try:
        query = "INSERT INTO food_items (item_name, price) VALUES (%s, %s)"
        cursor.execute(query, (item_name, price))
        db.commit()
        print("Food item added successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

def view_food_items():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    try:
        query = "SELECT * FROM food_items"
        cursor.execute(query)
        items = cursor.fetchall()
        for item in items:
            print(item)
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

# User Section
def user_menu(user_id):
    while True:
        print("\nUser Menu:")
        print("1. View Trains")
        print("2. Book Ticket")
        print("3. Order Food")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_trains()
        elif choice == "2":
            book_ticket(user_id)
        elif choice == "3":
            order_food(user_id)
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

def view_trains():
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    try:
        query = "SELECT * FROM trains"
        cursor.execute(query)
        trains = cursor.fetchall()
        for train in trains:
            print(train)
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

def book_ticket(user_id):
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    train_id = int(input("Enter train ID to book: "))
    seat_number = input("Enter seat number: ")

    try:
        query = "INSERT INTO tickets (user_id, train_id, seat_number) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, train_id, seat_number))
        db.commit()
        print("Ticket booked successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

def order_food(user_id):
    db = connect_to_database()
    if not db:
        print("Database connection failed!")
        return

    cursor = db.cursor()
    food_id = int(input("Enter food ID to order: "))
    quantity = int(input("Enter quantity: "))

    try:
        query = "INSERT INTO food_orders (user_id, food_id, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, food_id, quantity))
        db.commit()
        print("Food ordered successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        db.close()

# Main Program
def main():
    # Ensure schema is updated before the program starts
    update_user_table_schema()
    
    while True:
        print("\nTrain Database Management System")
        print("1. Admin Login")
        print("2. User Login")
        print("3. User Registration")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            if admin_login():
                admin_menu()
        elif choice == "2":
            user_id = user_login()
            if user_id:
                user_menu(user_id)
        elif choice == "3":
            user_register()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
