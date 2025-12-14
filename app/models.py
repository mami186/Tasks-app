from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from .database import Base
from sqlalchemy.orm import relationship

# Association table for many-to-many
task_tags = Table(
    "task_tags", Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    tags = relationship("Tag", back_populates="user", cascade="all, delete")
    tasks = relationship("Task", back_populates="user", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    body = Column(String, nullable=False)
    complete = Column(Boolean, default=False)
    pin = Column(Boolean, default=False)

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

    user = relationship("User", back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) 

    name  = Column(String, nullable=False)
    color = Column(String, nullable=False)

    tasks = relationship("Task", secondary=task_tags, back_populates="tags")
    user = relationship("User", back_populates="tags")
