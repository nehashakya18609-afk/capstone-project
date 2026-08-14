from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ==================================================
# TASK CREATE SCHEMA
# ==================================================

class TaskCreate(BaseModel):
    project_id: int
    title: str
    priority: str = Field(
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


# ==================================================
# TASK RESPONSE SCHEMA
# ==================================================

class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    priority: str
    due_date: Optional[str] = None

    class Config:
        from_attributes = True


# ==================================================
# AI QUICK-ADD REQUEST
# ==================================================

class QuickAddRequest(BaseModel):
    description: str = Field(
        min_length=1
    )
    project_id: int