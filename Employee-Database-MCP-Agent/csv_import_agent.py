import asyncio
import csv
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


BASE_DIR = Path(__file__).resolve().parent

python_path = BASE_DIR / "venv" / "Scripts" / "python.exe"
server_path = BASE_DIR / "csv_import_server.py"

transport = StdioTransport(
    command=str(python_path),
    args=[str(server_path)]
)

mcp_client = Client(transport)


def read_employee_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


async def import_employees(csv_path):
    employees = read_employee_csv(csv_path)

    if not employees:
        print("The CSV file does not contain employee records.")
        return

    async with mcp_client:
        result = await mcp_client.call_tool(
            "save_employee_records",
            {
                "employees": employees
            }
        )

    print(result.data)


async def main():
    file_name = input(
        "Enter CSV file name from the data folder: "
    ).strip()

    csv_path = BASE_DIR / "data" / file_name

    if not csv_path.exists():
        print("CSV file not found in the data folder.")
        return

    if csv_path.suffix.lower() != ".csv":
        print("Please provide a CSV file.")
        return

    await import_employees(csv_path)


if __name__ == "__main__":
    asyncio.run(main())