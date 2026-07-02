import csv
import os
import sqlite3

os.makedirs("database", exist_ok=True)

connection = sqlite3.connect("database/employees.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS employees")

cursor.execute("""
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    employee_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    department TEXT,
    designation TEXT,
    joining_date TEXT,
    manager TEXT,
    location TEXT,
    salary INTEGER
)
""")

with open(
    "data/employees.csv",
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    rows = []

    for row in reader:
        rows.append((
            row["employee_id"],
            row["employee_name"],
            row["email"],
            row["phone"],
            row["department"],
            row["designation"],
            row["joining_date"],
            row["manager"],
            row["location"],
            int(row["salary"])
        ))

cursor.executemany("""
INSERT INTO employees (
    employee_id,
    employee_name,
    email,
    phone,
    department,
    designation,
    joining_date,
    manager,
    location,
    salary
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

connection.commit()

connection.close()

print(f"Imported {len(rows)} employees into database/employees.db")