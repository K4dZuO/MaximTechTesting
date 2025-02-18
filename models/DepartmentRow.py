from pydantic import BaseModel, Field


class DepartmentRow(BaseModel):
    """Модель для единичной записи department"""
    
    departmentId: int = Field(ge=1)
    displayName: str