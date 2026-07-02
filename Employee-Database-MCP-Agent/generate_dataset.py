import csv
import os
import random

from faker import Faker

fake = Faker("en_IN")

os.makedirs("data", exist_ok=True)

departments = [
    "Engineering",
    "Human Resources",
    "Finance",
    "Marketing",
    "Sales",
    "Operations",
    "Data Science",
    "Customer Support"
]

designations = [
    "Software Engineer",
    "Senior Software Engineer",
    "Data Analyst",
    "HR Executive",
    "Finance Analyst",
    "Marketing Specialist",
    "Sales Executive",
    "Operations Manager"
]

locations = [
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Mumbai",
    "Pune",
    "Delhi"
]

managers = [
    "Ananya Sharma",
    "Vikram Kumar",
    "Priya Iyer",
    "Arjun Mehta",
    "Kavya Nair"
]

with open(
    "data/employees.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

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

    for number in range(1, 5001):

        writer.writerow([
            f"EMP{number:05d}",
            fake.name(),
            fake.email(),
            fake.phone_number(),
            random.choice(departments),
            random.choice(designations),
            fake.date_between(
                start_date="-8y",
                end_date="today"
            ).isoformat(),
            random.choice(managers),
            random.choice(locations),
            random.randint(350000, 1800000)
        ])

print("Created data/employees.csv with 5000 employee records.")