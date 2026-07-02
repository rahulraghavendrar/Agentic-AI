import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from google import genai


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")

gemini_client = genai.Client(api_key=api_key)

python_path = BASE_DIR / "venv" / "Scripts" / "python.exe"
server_path = BASE_DIR / "server.py"

transport = StdioTransport(
    command=str(python_path),
    args=[str(server_path)]
)

mcp_client = Client(transport)


def format_employee_with_gemini(employee):
    prompt = f"""
You are an Employee Details Assistant.

Format the following employee data in a neat and professional format.

Rules:
- Use the heading: Employee Profile
- Use clear labels and bullet points
- Do not invent or change values
- Do not mention tools, MCP, SQLite, or databases
- Format salary in Indian Rupees with commas
- Return only the formatted employee profile

Employee data:
{json.dumps(employee, indent=2)}
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


async def main():
    employee_id = input(
        "Enter employee ID (example: EMP00001): "
    ).strip().upper()

    async with mcp_client:
        result = await mcp_client.call_tool(
            "get_employee_details",
            {
                "employee_id": employee_id
            }
        )

    employee = result.data

    if "error" in employee:
        print("\nEmployee not found.")
        return

    formatted_employee = format_employee_with_gemini(employee)

    print("\n" + formatted_employee)


if __name__ == "__main__":
    asyncio.run(main())