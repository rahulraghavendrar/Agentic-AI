from fastmcp import FastMCP

from csv_database import save_employee_records as save_records_to_database


mcp = FastMCP("Employee CSV Import MCP Server")


@mcp.tool()
def save_employee_records(employees: list[dict]) -> dict:
    return save_records_to_database(employees)


if __name__ == "__main__":
    mcp.run()