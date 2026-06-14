from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    target_hours = Column(Integer, default=50)
    modules = relationship("Module", back_populates="subject")

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    name = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    subject = relationship("Subject", back_populates="modules")