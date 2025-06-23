from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

STATUS = {
    0: "Draft",
    1: "Publish"
}

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=0, nullable=False)
    blogs = relationship("Blog", back_populates="category")

    def __str__(self):
        return self.name

    def get_status_display(self):
        return STATUS.get(self.status, "Unknown")

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(Integer, default=0, nullable=False)

    category = relationship("Category", back_populates="blogs")

    def get_status_display(self):
        return STATUS.get(self.status, "Unknown")
