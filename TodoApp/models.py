from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
import json


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    def __repr__(self):
        # Create a dictionary of the object attributes
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'role': self.role
        }

        # `default=str` handles non-serializable types
        return json.dumps(user_dict, default=str)

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        # Create a dictionary of the object attributes
        todo_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'complete': self.complete,
            'owner_id': self.owner_id
        }

        # `default=str` handles non-serializable types
        return json.dumps(todo_dict, default=str)
