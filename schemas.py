from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ==================================================
# TASK SCHEMA
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
    description: str
    project_id: int