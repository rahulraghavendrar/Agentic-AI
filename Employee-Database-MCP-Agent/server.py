from fastmcp import FastMCP

from database import get_employee_by_id


mcp = FastMCP("Employee Database MCP Server")


@mcp.tool()
def get_employee_details(employee_id: str) -> dict:
    """
    Get details of one employee using the employee ID.

    Example employee ID: EMP00001
    """

    employee_id = employee_id.strip().upper()

    employee = get_employee_by_id(employee_id)

    if employee is None:
        return {
            "error": f"Employee with ID {employee_id} was not found."
        }

    return employee


if __name__ == "__main__":
    mcp.run()