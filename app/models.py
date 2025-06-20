from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean,ForeignKey
from .database import Base
from sqlalchemy import func
from sqlalchemy.orm import relationship




class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False,index=True )
    content = Column(Text, nullable=False)
    published = Column(Boolean, nullable=False, server_default="1") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


# create a model for usercreate

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # <-- EMAIL field
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"


