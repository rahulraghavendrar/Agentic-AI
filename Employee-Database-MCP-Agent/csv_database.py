import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "employees.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_employees_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
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

    connection.commit()
    connection.close()


def save_employee_records(employees):
    create_employees_table()

    connection = get_connection()
    cursor = connection.cursor()

    saved_count = 0
    skipped_count = 0

    for employee in employees:
        employee_id = employee.get("employee_id", "").strip().upper()
        employee_name = employee.get("employee_name", "").strip()

        if not employee_id or not employee_name:
            skipped_count += 1
            continue

        try:
            cursor.execute("""
            INSERT OR REPLACE INTO employees (
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
            """, (
                employee_id,
                employee_name,
                employee.get("email", "").strip(),
                employee.get("phone", "").strip(),
                employee.get("department", "").strip(),
                employee.get("designation", "").strip(),
                employee.get("joining_date", "").strip(),
                employee.get("manager", "").strip(),
                employee.get("location", "").strip(),
                int(employee.get("salary", 0) or 0)
            ))

            saved_count += 1

        except ValueError:
            skipped_count += 1

    connection.commit()
    connection.close()

    return {
        "message": "Employee import completed",
        "saved_records": saved_count,
        "skipped_records": skipped_count
    }