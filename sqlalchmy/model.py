# 3 using SQLAlchemy to define our User model and create the database tables

from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
import time
from sqlalchemy.orm import relationship


# SQLAlchemy model for the Post table, inheriting from the Base class defined in database.py
# This class defines the structure of the "posts" table in the database, with columns for id, title, content, and published status.
# Each column is defined using SQLAlchemy's Column class, specifying the data type and any constraints (e.g., primary key, nullable).
# it is different from the pydantic schemas in schemas.py which are used for request validation and response formatting. 
# The SQLAlchemy model is used to interact with the database, while the pydantic schemas are used to validate and serialize data for API requests and responses.

class Post(Base):
    __tablename__ = "posts"                             # name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # unique identifier for each post
    title = Column(String, nullable=False)              # post's title, cannot be null
    content = Column(String, nullable=False)            # post's content, cannot be null
    published = Column(Integer, default=1)              # published status, default is 1 (published)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer, ForeignKey("writer.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User") 

class User(Base):
    __tablename__ = "writer"                            # name of the table in the database
    id = Column(Integer, primary_key=True, index=True)  # unique identifier for each user
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())  # timestamp of post creation, default is current time


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("writer.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



class Account(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20))
    college = Column(String(20))
    age = Column(Integer)