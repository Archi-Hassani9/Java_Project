import mysql.connector as ms
from getpass import getpass

#Global variables
db = 'Appointment_Booking_System'

#function to connect MySQL qith Python
def ConnectDB():
    return ms.connect(host='localhost',user='root',password='MYSQL@93',database=db)
    

#function to Create database
def create_database():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS DoctorAppointmentDB")
    cursor.execute("USE DoctorAppointmentDB")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'doctor', 'patient') NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            specialization VARCHAR(255) NOT NULL,
            available_slots TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            doctor_id INT,
            appointment_date DATETIME,
            status ENUM('scheduled', 'cancelled') DEFAULT 'scheduled',
            FOREIGN KEY (patient_id) REFERENCES users(user_id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            appointment_id INT,
            amount DECIMAL(10,2),
            status ENUM('pending', 'completed') DEFAULT 'pending',
            FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
        )
    """)
    mydb.commit()
    cursor.close()
    mydb.close()

def register_user():
    mydb = connect_db()
    cursor = mydb.cursor()
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    role = input("Enter role (admin/doctor/patient): ")
    
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    mydb.commit()
    print("Registration successful!")
    cursor.close()
    mydb.close()

def login():
    db = connect_db_with_schema()
    cursor = db.cursor()
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        print(f"Login successful! Welcome {user[1]}")
        return user
    else:
        print("Invalid credentials!")
        return None
 
def cancel_appointment():
    mydb = connect_db()
    cursor = mydb.cursor()
    appointment_id = int(input("Enter the appointment ID to cancel: "))
    
    cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    
    if appointment:
        cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE appointment_id = %s", (appointment_id,))
        mydb.commit()
        print("Appointment cancelled successfully!")
    else:
        print("Appointment not found!")
    
    cursor.close()
    mydb.close()

def cancel_appointment(patient_id):
    db = connect_db_with_schema()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM appointments WHERE patient_id = %s AND status = 'scheduled'", (patient_id,))
    appointments = cursor.fetchall()
    
    if not appointments:
        print("No scheduled appointments found.")
        return
    
    for app in appointments:
        print(f"Appointment ID: {app[0]}, Doctor ID: {app[2]}, Date: {app[3]}")
    
    appointment_id = int(input("Enter Appointment ID to cancel: "))
    cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE appointment_id = %s", (appointment_id,))
    db.commit()
    print("Appointment cancelled successfully!")
    
    cursor.close()
    db.close()

def make_payment(appointment_id, amount):
    db = connect_db_with_schema()
    cursor = db.cursor()
    cursor.execute("INSERT INTO payments (appointment_id, amount, status) VALUES (%s, %s, 'completed')", (appointment_id, amount))
    db.commit()
    print("Payment successful!")
    
    cursor.close()
    db.close()

def MainMenu():
    print('M A I N   M E N U')
    print('0. EXIT.')
    print('1. Registration')
    print('2. Login')
    print('3. Doctor Information')
    print('4. Book Appointment')
    print('5. Cancel Appointment')
    print('6. Payment Information')
    ch = int(input('Enter your Choice: '))
    return ch

#MAIN MENU of the Project
if __name__ == '__main__':
    while True:
        mydb = ConnectDB()
        cur = mydb.cursor(dictionary=True)
        CreateDB()
        ch = MainMenu()
        if ch == 0:
            exit()
        elif ch == 1:
            register_user()
        elif ch == 5:
            cancel_appointment()
        else:
            print('INVALID CHOICE !!!')
        input('press ENTER to get back to MAIN MENU...')

def MainMenu():
    print('M A I N   M E N U')
    print('0. EXIT.')
    print('1. Registration')
    print('2. Login')
    print('3. Doctor Information')
    print('4. Book Appointment')
    print('5. Cancel Appointment')
    print('6. Payment Information')
    ch = int(input('Enter your Choice: '))
    return ch

#MAIN MENU of the Project
if __name__ == '__main__':
    while True:
        mydb = ConnectDB()
        cur = mydb.cursor(dictionary=True)
        CreateDB()
        ch = MainMenu()
        if ch==0:
            exit()
        elif ch==1:
            register_user()
        else:
            print('INVALID CHOICE !!!')
        input('press ENTER to get back to MAIN MENU...')

def main():
    while True:
        print("\nDoctor Appointment Booking System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            register_user()
        elif choice == "2":
            user = login()
            if user:
                if user[3] == 'patient':
                    while True:
                        print("\nPatient Menu")
                        print("1. Book Appointment")
                        print("2. Cancel Appointment")
                        print("3. Make Payment")
                        print("4. Logout")
                        action = input("Enter choice: ")
                        if action == "1":
                            book_appointment(user[0])
                        elif action == "2":
                            cancel_appointment(user[0])
                        elif action == "3":
                            appointment_id = int(input("Enter Appointment ID: "))
                            amount = float(input("Enter Payment Amount: "))
                            make_payment(appointment_id, amount)
                        elif action == "4":
                            break
                elif user[3] == 'admin':
                    admin_panel()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

