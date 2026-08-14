
from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(100), nullable=False, default="Poonam")

    projects = relationship(
        "Project",
        back_populates="owner"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    name = Column(
        String(255),
        nullable=False,
        default="Capstone"
    )

    owner = relationship(
        "User",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    priority = Column(
        String(10),
        nullable=False
    )

    due_date = Column(
        Text,
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="check_task_priority"
        ),
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

