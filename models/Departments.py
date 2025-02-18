from pydantic import BaseModel
from typing import List


from .DepartmentRow import DepartmentRow

class Departments(BaseModel):
    """Модель для получения списка Department"""
    
    departments: List[DepartmentRow]