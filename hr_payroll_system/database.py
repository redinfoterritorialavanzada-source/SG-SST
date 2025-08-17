from typing import List, Dict
from models.employee import Employee

# In-memory database
_employees: Dict[str, Employee] = {}

def add_employee(employee: Employee) -> None:
    """Adds an employee to the database."""
    _employees[str(employee.id)] = employee

def get_employee(employee_id: str) -> Employee | None:
    """Gets an employee by their ID."""
    return _employees.get(employee_id)

def list_employees() -> List[Employee]:
    """Lists all employees."""
    return list(_employees.values())

def reset_employees() -> None:
    """Clears all employees from the database (for testing)."""
    _employees.clear()
