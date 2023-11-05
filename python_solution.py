import sqlite3
from sqlite3 import Error
from datetime import datetime

def create_database():
    conn = None
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            cursor.execute('''CREATE TABLE IF NOT EXISTS Director (
                Director_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Passport TEXT NOT NULL,
                YearOfBirth INTEGER)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS DistributionFirm (
                id_Firm INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Address TEXT,
                Director_id INTEGER NOT NULL,
                Division_id INTEGER NOT NULL)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Storage (
                id_Storage INTEGER PRIMARY KEY AUTOINCREMENT,
                Address TEXT,
                Volume INTEGER,
                NameOfFirm TEXT NOT NULL)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Item (
                id_Item INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Price REAL,
                Firm TEXT NOT NULL,
                Quantity INTEGER,
                Conditions TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Food (
                id_Food INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Firm TEXT NOT NULL,
                ExpirationDate TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Equipment (
                id_Equipment INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Firm TEXT NOT NULL,
                Characteristics TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Division (
                id_Division INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                NumberOfWorkers INTEGER)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Respon (
                id_Respon INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                NumberOfRespon INTEGER)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Worker (
                id_Worker INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Sex TEXT,
                YearOfBirth INTEGER,
                Passport TEXT NOT NULL,
                Experience TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Division_Respon_Worker (
                Division_id INTEGER,
                Responsibility_id INTEGER,
                Worker_id INTEGER,
                PRIMARY KEY (Division_id, Responsibility_id, Worker_id))''')

            # Заповнюємо таблиці даними
            cursor.execute("INSERT INTO Director (Name, Passport, YearOfBirth) VALUES (?, ?, ?)", ('John Doe', 'AB123456', 1980))
            cursor.execute("INSERT INTO Director (Name, Passport, YearOfBirth) VALUES (?, ?, ?)", ('Jane Smith', 'CD789012', 1975))

            cursor.execute("INSERT INTO DistributionFirm (Name, Address, Director_id, Division_id) VALUES (?, ?, ?, ?)", ('Firm A', '123 Main St', 1, 1))
            cursor.execute("INSERT INTO DistributionFirm (Name, Address, Director_id, Division_id) VALUES (?, ?, ?, ?)", ('Firm B', '456 Elm St', 2, 2))
            cursor.execute("INSERT INTO DistributionFirm (Name, Address, Director_id, Division_id) VALUES (?, ?, ?, ?)", ('Firm C', '789 Oak St', 2, 2))

            cursor.execute("INSERT INTO Storage (Address, Volume, NameOfFirm) VALUES (?, ?, ?)", ('789 Oak St', 1000, 'Firm C'))
            cursor.execute("INSERT INTO Storage (Address, Volume, NameOfFirm) VALUES (?, ?, ?)", ('101 Pine St', 800, 'Firm D'))

            cursor.execute("INSERT INTO Item (Name, Price, Firm, Quantity, Conditions) VALUES (?, ?, ?, ?, ?)", ('Item 1', 10.0, 'Firm A', 100, 'Good'))
            cursor.execute("INSERT INTO Item (Name, Price, Firm, Quantity, Conditions) VALUES (?, ?, ?, ?, ?)", ('Item 2', 15.0, 'Firm B', 75, 'Excellent'))
            cursor.execute("INSERT INTO Item (Name, Price, Firm, Quantity, Conditions) VALUES (?, ?, ?, ?, ?)", ('Food 1', 15.0, 'Firm C', 85, 'Excellent'))

            cursor.execute("INSERT INTO Food (Name, Firm, ExpirationDate) VALUES (?, ?, ?)", ('Food 1', 'Firm C', '2023-12-31'))
            cursor.execute("INSERT INTO Food (Name, Firm, ExpirationDate) VALUES (?, ?, ?)", ('Food 2', 'Firm B', '2024-06-30'))

            cursor.execute("INSERT INTO Equipment (Name, Firm, Characteristics) VALUES (?, ?, ?)", ('Equipment 1', 'Firm A', 'High capacity'))
            cursor.execute("INSERT INTO Equipment (Name, Firm, Characteristics) VALUES (?, ?, ?)", ('Equipment 2', 'Firm B', 'Compact design'))

            cursor.execute("INSERT INTO Division (Name, NumberOfWorkers) VALUES (?, ?)", ('Division 1', 10))
            cursor.execute("INSERT INTO Division (Name, NumberOfWorkers) VALUES (?, ?)", ('Division 2', 8))

            cursor.execute("INSERT INTO Respon (Name, NumberOfRespon) VALUES (?, ?)", ('Responsibility 1', 5))
            cursor.execute("INSERT INTO Respon (Name, NumberOfRespon) VALUES (?, ?)", ('Responsibility 2', 3))

            cursor.execute("INSERT INTO Worker (Name, Sex, YearOfBirth, Passport, Experience) VALUES (?, ?, ?, ?, ?)", ('Worker 1', 'Male', 1985, 'EF345678', '5 years'))
            cursor.execute("INSERT INTO Worker (Name, Sex, YearOfBirth, Passport, Experience) VALUES (?, ?, ?, ?, ?)", ('Worker 2', 'Female', 1990, 'GH901234', '3 years'))

            cursor.execute("INSERT INTO Division_Respon_Worker (Division_id, Responsibility_id, Worker_id) VALUES (?, ?, ?)", (1, 1, 1))
            cursor.execute("INSERT INTO Division_Respon_Worker (Division_id, Responsibility_id, Worker_id) VALUES (?, ?, ?)", (2, 2, 2))

            conn.commit()
        return conn
    except Error as e:
        print(e)
        return None

def execute_queries(conn):
    cursor = conn.cursor()
    
    # Виконання першого SQL-запиту
    cursor.execute("SELECT * FROM Item INNER JOIN Food ON Item.Name = Food.Name WHERE Food.Name = 'Food 1';")
    result1 = cursor.fetchall()
    
    print("Результат першого запиту:")
    for row in result1:
        print(row)

    # Виконання другого SQL-запиту
    cursor.execute("SELECT * FROM DistributionFirm INNER JOIN Storage ON DistributionFirm.Name = Storage.NameOfFirm WHERE Storage.Address = '789 Oak St';")
    result2 = cursor.fetchall()

    print("\nРезультат другого запиту:")
    for row in result2:
        print(row)

def update_records_and_reexecute_queries(conn):
    cursor = conn.cursor()
    
    #Отримуємо поточний час, щоб виконати умову завдання по оновленню записів у таблиці
    current_time = datetime.now().strftime('%H%M%S')

    # Оновлюємо записи у таблиці Item
    cursor.execute("UPDATE Item SET Price = ? WHERE Name = 'Food 1';", (current_time,))
    conn.commit()

    execute_queries(conn)

def main():
    conn = create_database()
    if conn is None:
        return

    while True:
        print("Меню:")
        print("1. Виконати SQL-запити")
        print("2. Оновити та виконати запити")
        print("3. Вихід")

        choice = input("Оберіть дію (1/2/3): ")

        if choice == "1":
            execute_queries(conn)
        elif choice == "2":
            update_records_and_reexecute_queries(conn)
        elif choice == "3":
            conn.close()
            break
        else:
            print("Неправильний вибір. Будь ласка, оберіть 1, 2 чи 3.")

if __name__ == '__main__':
    main()
