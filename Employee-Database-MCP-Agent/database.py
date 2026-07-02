import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "employees.db"


def get_employee_by_id(employee_id):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
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
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))

    employee = cursor.fetchone()

    connection.close()

    if employee is None:
        return None

    return dict(employee)


if __name__ == "__main__":
    employee = get_employee_by_id("EMP00001")
    print(employee)