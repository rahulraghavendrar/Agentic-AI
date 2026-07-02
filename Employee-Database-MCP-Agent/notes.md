# Employee Database MCP Agent

## Project Goal

This project implements an AI-powered Employee Database Agent using **Gemini**, **FastMCP**, and **SQLite**.

The user provides an **Employee ID**, and the agent retrieves that employee's information from a SQL database using an **MCP Tool**. The retrieved information is then sent to **Gemini**, which formats the output into a clean and readable employee profile.

---

# Overall Workflow

```text
                 User
                   │
                   ▼
        Enter Employee ID
                   │
                   ▼
         Gemini Employee Agent
                   │
                   ▼
             MCP Client
                   │
                   ▼
        MCP Tool (get_employee_details)
                   │
                   ▼
            SQLite Database
                   │
                   ▼
          Employee Information
                   │
                   ▼
          Gemini Formatting
                   │
                   ▼
        Formatted Employee Profile
```

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Faker | Generate fake employee records |
| CSV | Store generated employee data |
| SQLite | SQL Database |
| FastMCP | Create MCP Server and MCP Tool |
| Gemini API | Format employee details |
| python-dotenv | Read API key from `.env` |

---

# Project Structure

```text
Employee-Database-MCP-Agent/
│
├── data/
│   └── employees.csv
│
├── database/
│   └── employees.db
│
├── generate_dataset.py
├── import_data.py
├── database.py
├── server.py
├── agent.py
├── requirements.txt
├── notes.md
└── .env
```

---

# Step 1 - Generate Employee Dataset

## File

```text
generate_dataset.py
```

### Purpose

This file generates a realistic employee dataset using the **Faker** library.

Each employee contains:

- Employee ID
- Name
- Email
- Phone
- Department
- Designation
- Joining Date
- Manager
- Location
- Salary

Example:

```text
EMP00001
Rahul Kumar
Engineering
Software Engineer
```

The generated dataset is saved as

```text
data/employees.csv
```

Approximately **5000 employee records** are generated.

---

# Step 2 - Import Data into SQLite

## File

```text
import_data.py
```

### Purpose

Reads the employee CSV file and inserts every record into a SQLite database.

Creates:

```text
database/employees.db
```

Creates SQL table:

```sql
employees
```

The SQLite database now stores all employee information.

---

# Step 3 - Retrieve Employee Details

## File

```text
database.py
```

Main function:

```python
get_employee_by_id(employee_id)
```

Example SQL Query:

```sql
SELECT *
FROM employees
WHERE employee_id = ?
```

Using `?` keeps the query safe from SQL Injection.

### Returns

If employee exists:

```python
{
    "employee_id": "EMP00001",
    "employee_name": "Rahul Kumar",
    "department": "Engineering"
}
```

If employee doesn't exist:

```python
None
```

---

# Step 4 - Build the MCP Tool

## File

```text
server.py
```

## What is MCP?

MCP stands for

> **Model Context Protocol**

It provides a standard way for AI agents to access external tools.

Instead of the AI directly accessing the database, the AI communicates through an MCP Tool.

Our MCP Tool is

```text
get_employee_details
```

Input

```json
{
  "employee_id": "EMP00001"
}
```

Output

```json
{
  "employee_id": "EMP00001",
  "employee_name": "Rahul Kumar",
  "department": "Engineering",
  "designation": "Software Engineer"
}
```

The tool returns only the requested employee.

---

# Step 5 - Test Using MCP Inspector

Before connecting Gemini, the MCP Tool was tested independently.

The Inspector connected to

```text
server.py
```

The following input was tested

```json
{
  "employee_id": "EMP00001"
}
```

The response successfully returned one employee from SQLite.

This verified that

- MCP Server works
- SQLite retrieval works
- Tool communication works

---

# Step 6 - Build the Gemini Agent

## File

```text
agent.py
```

The agent performs the following steps.

### Step 1

Ask the user for an Employee ID.

Example

```text
EMP00001
```

↓

### Step 2

The FastMCP Client starts the MCP Server.

↓

### Step 3

The client calls

```text
get_employee_details
```

↓

### Step 4

The MCP Tool queries SQLite.

↓

### Step 5

SQLite returns one employee.

↓

### Step 6

The employee JSON is sent to Gemini.

↓

### Step 7

Gemini formats the response into a professional employee profile.

Example Output

```text
Employee Profile

Employee ID : EMP00001

Name         : Rahul Kumar

Department   : Engineering

Designation  : Software Engineer

Email        : rahul@gmail.com

Phone        : 9876543210

Joining Date : 2024-06-15

Manager      : Ananya Sharma

Location     : Chennai

Salary       : ₹8,50,000
```

---

# Why Use MCP?

Without MCP

```text
Gemini
     │
     ▼
SQLite Database
```

The AI must know how to communicate with the database.

With MCP

```text
Gemini
     │
     ▼
MCP Tool
     │
     ▼
SQLite Database
```

Benefits

- Clean architecture
- Reusable tools
- Easier testing
- Easier maintenance
- Secure separation between AI and database

---

# Security

The Gemini API key is stored inside

```text
.env
```

Example

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file must **never** be pushed to GitHub.

---

# .gitignore

```gitignore
.env
*.env
venv/
__pycache__/
database/*.db
```

This prevents:

- API Keys
- Database
- Virtual Environment
- Python Cache

from being uploaded.

---

# Commands Used

## Generate Dataset

```powershell
.\venv\Scripts\python.exe generate_dataset.py
```

---

## Import into SQLite

```powershell
.\venv\Scripts\python.exe import_data.py
```

---

## Test Database

```powershell
.\venv\Scripts\python.exe database.py
```

---

## Run MCP Server

```powershell
.\venv\Scripts\python.exe server.py
```

---

## Run Gemini Agent

```powershell
.\venv\Scripts\python.exe agent.py
```

---

# Final Architecture

```text
                     User
                       │
                       ▼
              Enter Employee ID
                       │
                       ▼
               Gemini AI Agent
                       │
                       ▼
                 FastMCP Client
                       │
                       ▼
        MCP Tool (get_employee_details)
                       │
                       ▼
              SQLite Employee Database
                       │
                       ▼
            Employee Details (JSON)
                       │
                       ▼
             Gemini Response Formatter
                       │
                       ▼
        Professional Employee Profile
```

---

# Outcome

This project successfully demonstrates:

- Fake Employee Dataset Generation
- SQL Database Creation
- SQL Querying
- MCP Tool Development
- MCP Client Communication
- Gemini API Integration
- AI-powered Employee Information Retrieval
- Clean, modular Agentic AI architecture