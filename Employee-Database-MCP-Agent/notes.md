# Employee Database MCP Agent

## Project Goal

This project is an Agentic AI system for managing employee records.

It supports two workflows:

1. Retrieve one employee’s details using an employee ID.
2. Read employee records from a CSV file and save them into a SQLite database through an MCP tool.

The project uses:

- Python
- SQLite
- FastMCP
- Gemini API
- CSV files
- Faker

---

# Overall Architecture

```text
Employee CSV File
        ↓
CSV Import Agent
        ↓
MCP Save Tool
        ↓
SQLite Employee Database
        ↓
MCP Retrieval Tool
        ↓
Gemini Employee Agent
        ↓
Formatted Employee Profile
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Faker | Generate fake employee records |
| CSV | Store and import employee data |
| SQLite | Store employee records in a SQL database |
| FastMCP | Build MCP servers, tools, and clients |
| Gemini API | Format retrieved employee data neatly |
| python-dotenv | Load the Gemini API key from `.env` |

---

# Project Structure

```text
Employee-Database-MCP-Agent/
│
├── data/
│   ├── employees.csv
│   └── new_employees.csv
│
├── database/
│   └── employees.db
│
├── generate_dataset.py
├── create_100_employees.py
├── import_data.py
├── database.py
├── server.py
├── agent.py
├── csv_database.py
├── csv_import_server.py
├── csv_import_agent.py
├── start_mcp_server.bat
├── requirements.txt
├── notes.md
└── .env
```

---

# Feature 1: Employee Retrieval Agent

## Goal

The user enters an employee ID, such as:

```text
EMP00001
```

The agent retrieves only that employee’s record from SQLite and prints it in a clean format.

---

## Retrieval Workflow

```text
User enters Employee ID
        ↓
Gemini Employee Agent
        ↓
MCP Client
        ↓
MCP Tool: get_employee_details
        ↓
SQLite Database
        ↓
Employee JSON
        ↓
Gemini formats the result
        ↓
Neat Employee Profile in Terminal
```

---

## Dataset Generation

### File

```text
generate_dataset.py
```

This file uses Faker to create a large employee dataset.

Each employee record contains:

- Employee ID
- Employee Name
- Email
- Phone
- Department
- Designation
- Joining Date
- Manager
- Location
- Salary

The generated dataset is saved in:

```text
data/employees.csv
```

---

## Initial CSV to SQLite Import

### File

```text
import_data.py
```

This file reads `data/employees.csv` and inserts employee records into:

```text
database/employees.db
```

The SQLite table is:

```text
employees
```

---

## Database Retrieval Logic

### File

```text
database.py
```

Important function:

```python
get_employee_by_id(employee_id)
```

It runs a safe SQL query:

```sql
SELECT *
FROM employees
WHERE employee_id = ?
```

The `?` placeholder safely passes the employee ID into SQL and helps prevent SQL injection.

If an employee exists, the function returns a Python dictionary.

Example:

```python
{
    "employee_id": "EMP00001",
    "employee_name": "Rahul Kumar",
    "department": "Engineering",
    "designation": "Software Engineer"
}
```

If the employee does not exist, it returns:

```python
None
```

---

## Retrieval MCP Server

### File

```text
server.py
```

MCP means:

```text
Model Context Protocol
```

MCP allows an AI agent to access external tools through a standard interface.

The retrieval MCP tool is:

```text
get_employee_details
```

Example input:

```json
{
  "employee_id": "EMP00001"
}
```

Example output:

```json
{
  "employee_id": "EMP00001",
  "employee_name": "Rahul Kumar",
  "department": "Engineering",
  "designation": "Software Engineer"
}
```

The tool returns only the requested employee record.

---

## MCP Inspector Testing

The MCP Inspector was used to test `server.py` before connecting it to Gemini.

The tool was tested using:

```json
{
  "employee_id": "EMP00001"
}
```

This confirmed that:

- The MCP server works.
- The retrieval tool works.
- SQLite retrieval works.
- The employee data is returned correctly.

---

## Gemini Employee Agent

### File

```text
agent.py
```

The Gemini agent performs these steps:

1. Ask the user for an employee ID.
2. Start the retrieval MCP server using `StdioTransport`.
3. Call `get_employee_details`.
4. Receive employee JSON from SQLite.
5. Send the employee JSON to Gemini.
6. Gemini formats the details clearly.
7. Print the formatted employee profile in the terminal.

Run it with:

```powershell
.\venv\Scripts\python.exe agent.py
```

Example input:

```text
EMP00001
```

Example output:

```text
Employee Profile

- Employee ID: EMP00001
- Name: Rahul Kumar
- Department: Engineering
- Designation: Software Engineer
- Email: rahul@example.com
- Phone: 9876543210
- Joining Date: 2024-06-15
- Manager: Ananya Sharma
- Location: Chennai
- Salary: ₹8,50,000
```

---

# Feature 2: CSV Import Agent

## Goal

This feature allows the user to provide an employee CSV file.

The system reads the CSV file, converts each row into a JSON-style Python dictionary, and sends all employee records to an MCP save tool.

The MCP tool inserts those records into SQLite.

---

## CSV Import Workflow

```text
Employee CSV File
        ↓
csv_import_agent.py
        ↓
CSV rows converted into employee dictionaries
        ↓
MCP Tool: save_employee_records
        ↓
SQLite employees table
        ↓
Employee records saved or updated
```

---

## Generate a Small Test CSV

### File

```text
create_100_employees.py
```

This file creates a CSV file containing 100 employee records.

Output file:

```text
data/new_employees.csv
```

Run it with:

```powershell
.\venv\Scripts\python.exe create_100_employees.py
```

This avoids downloading files and is useful when the C: drive has low disk space.

---

## CSV Database Save Logic

### File

```text
csv_database.py
```

This file is separate from the original `database.py`.

It contains:

```python
save_employee_records(employees)
```

The function:

1. Creates the `employees` table if it does not exist.
2. Receives employee records as a list of dictionaries.
3. Validates that each record has an employee ID and employee name.
4. Uses SQLite to insert or update records.
5. Returns the number of saved and skipped records.

The SQL command uses:

```sql
INSERT OR REPLACE INTO employees
```

This means:

- New employee IDs are inserted.
- Existing employee IDs are updated.
- Duplicate employee IDs do not create duplicate rows.

---

## CSV Import MCP Server

### File

```text
csv_import_server.py
```

This is a separate MCP server created only for importing employee records.

It provides this MCP tool:

```text
save_employee_records
```

Tool input structure:

```json
{
  "employees": [
    {
      "employee_id": "EMP05001",
      "employee_name": "Aarav Sharma",
      "department": "Engineering"
    }
  ]
}
```

The MCP tool sends the employee records to `csv_database.py`, which saves them into SQLite.

---

## CSV Import Agent

### File

```text
csv_import_agent.py
```

This agent performs these steps:

1. Ask the user for a CSV filename.
2. Look for that file inside the `data` folder.
3. Read the CSV using Python’s built-in `csv.DictReader`.
4. Convert every CSV row into a dictionary.
5. Start `csv_import_server.py` using `StdioTransport`.
6. Call the MCP tool `save_employee_records`.
7. Print the import result.

Run it with:

```powershell
.\venv\Scripts\python.exe csv_import_agent.py
```

When prompted, enter:

```text
new_employees.csv
```

Expected output:

```text
{
    "message": "Employee import completed",
    "saved_records": 100,
    "skipped_records": 0
}
```

---

## Verify Imported Records

After importing CSV records, use the existing Gemini retrieval agent:

```powershell
.\venv\Scripts\python.exe agent.py
```

Enter an imported employee ID:

```text
EMP05001
```

The existing retrieval MCP tool reads the newly saved employee from the same SQLite database, and Gemini formats the profile.

This proves that both workflows use the same employee database.

---

# Why Two MCP Servers Were Used

The original working files were not replaced.

The project now has two focused MCP servers:

| MCP Server | Tool | Purpose |
|---|---|---|
| `server.py` | `get_employee_details` | Retrieve one employee by ID |
| `csv_import_server.py` | `save_employee_records` | Save employee records from CSV |

This keeps the project modular.

```text
Retrieval MCP Server → Read employee details
Import MCP Server    → Save employee records
```

---

# Security

The Gemini API key is stored in:

```text
.env
```

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file must never be pushed to GitHub.

The local SQLite database should also not be pushed because it can be regenerated from CSV files.

---

# Commands Summary

## Generate the original employee dataset

```powershell
.\venv\Scripts\python.exe generate_dataset.py
```

## Import the original CSV into SQLite

```powershell
.\venv\Scripts\python.exe import_data.py
```

## Run the Gemini retrieval agent

```powershell
.\venv\Scripts\python.exe agent.py
```

## Generate 100 test employee records

```powershell
.\venv\Scripts\python.exe create_100_employees.py
```

## Run the CSV import agent

```powershell
.\venv\Scripts\python.exe csv_import_agent.py
```

---

# Final Architecture

```text
CSV File
    ↓
CSV Import Agent
    ↓
CSV Import MCP Server
    ↓
SQLite Employee Database
    ↓
Retrieval MCP Server
    ↓
Gemini Employee Agent
    ↓
Formatted Employee Profile
```

---

# Final Result

This project now demonstrates:

- Employee dataset generation
- CSV file processing
- CSV row to JSON conversion
- SQLite database storage
- SQL insert and update operations
- MCP save tool
- MCP retrieval tool
- MCP client communication
- Gemini API integration
- AI-formatted employee profiles
- Modular Agentic AI architecture