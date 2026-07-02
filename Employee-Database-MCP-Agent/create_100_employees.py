import csv
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "new_employees.csv"

names = [
    "Aarav Sharma", "Meera Iyer", "Rohan Kumar", "Ananya Rao",
    "Vikram Singh", "Kavya Nair", "Arjun Mehta", "Priya Patel",
    "Rahul Verma", "Sneha Reddy", "Aditya Joshi", "Neha Gupta",
    "Karan Malhotra", "Divya Menon", "Sanjay Das", "Pooja Shah",
    "Nikhil Bansal", "Isha Kapoor", "Manoj Yadav", "Aditi Kulkarni"
]

departments = [
    "Engineering", "Data Science", "Finance", "Human Resources",
    "Marketing", "Sales", "Operations", "Customer Support"
]

designations = [
    "Software Engineer", "Data Analyst", "Finance Analyst", "HR Executive",
    "Marketing Specialist", "Sales Executive", "Operations Manager",
    "Support Engineer"
]

managers = [
    "Ananya Sharma", "Vikram Kumar", "Priya Iyer",
    "Arjun Mehta", "Kavya Nair"
]

locations = [
    "Chennai", "Bengaluru", "Hyderabad",
    "Mumbai", "Pune", "Delhi"
]

with open(CSV_PATH, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "employee_id",
        "employee_name",
        "email",
        "phone",
        "department",
        "designation",
        "joining_date",
        "manager",
        "location",
        "salary"
    ])

    for i in range(1, 101):
        name = names[(i - 1) % len(names)]

        writer.writerow([
            f"EMP{5000 + i:05d}",
            name,
            f"{name.lower().replace(' ', '.')}{i}@example.com",
            f"9{800000000 + i:09d}",
            departments[(i - 1) % len(departments)],
            designations[(i - 1) % len(designations)],
            (date(2020, 1, 1) + timedelta(days=i * 17)).isoformat(),
            managers[(i - 1) % len(managers)],
            locations[(i - 1) % len(locations)],
            450000 + ((i * 17000) % 950000)
        ])

print(f"Created CSV file: {CSV_PATH}")