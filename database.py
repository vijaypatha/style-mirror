from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import json


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    profession = Column(String)
    style_analysis = Column(Text, nullable=True)
    autopilot_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    responses = relationship("TrainingResponse", back_populates="user")
    customers = relationship("Customer", back_populates="user")

class TrainingResponse(Base):
    __tablename__ = "training_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="responses")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="customers")
    notes = relationship("CustomerNote", back_populates="customer")
    messages = relationship("Message", back_populates="customer")

class CustomerNote(Base):
    __tablename__ = "customer_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="notes")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    content = Column(Text)
    type = Column(String)  # "sms" or "email"
    status = Column(String)  # "draft", "autopilot", "sent", "dismissed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="messages")

class CommunicationOpportunity(Base):
    __tablename__ = "communication_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    trigger = Column(String)
    timing = Column(String)  # "immediate", "this_week", "this_month"
    medium = Column(String)  # "sms" or "email"
    reference = Column(Text)
    importance = Column(Integer)  # 1-10
    status = Column(String)  # "pending", "processed", "dismissed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer")

# Create database
DATABASE_URL = "sqlite:///./style_mirror.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()