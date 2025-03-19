from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy

from backend import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Date, Table, UniqueConstraint, \
    PrimaryKeyConstraint, inspect
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        columns = inspect(self.__class__).columns.keys()
        result = {}
        for column in columns:
            value = getattr(self, column)
            if isinstance(value, datetime):
                result[column] = value.isoformat()
            elif isinstance(value, date):
                result[column] = value.isoformat()
            else:
                result[column] = value
        return result

class BasePicModel(BaseModel):
    __abstract__ = True  # Marked as an abstract class

    # Defines an internal field to store the actual photo URL value
    _pic_url = Column("pic_url", String(255))

    @property
    def pic_url(self):
        # Returns the complete path when accessing the photo URL
        return self._pic_url

    @pic_url.setter
    def pic_url(self, value):
        # When setting the photo URL, automatically adds path to the front
        if value and not value.startswith("/uploaded_Pic/"):
            self._pic_url = f"/uploaded_Pic/{value}"
        else:
            self._pic_url = value


# User Model
class User(BasePicModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    memorials = relationship("Memorial", back_populates="creator", cascade="all, delete-orphan")
    memorial_user_links = relationship("MemorialUser", back_populates="user", cascade="all, delete-orphan")
    invited_keys = relationship("InviteKey", back_populates="user", cascade="all, delete-orphan")
    user_offerings = relationship("UserOffering", back_populates="user", cascade="all, delete-orphan")
    memorial_offerings = relationship("MemorialOffering", back_populates="user", cascade="all, delete-orphan")
    memorial_messages = relationship("MemorialMessage", back_populates="user", cascade="all, delete-orphan")
    remembrance_messages = relationship("RemembranceMessage", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Memorial Hall Model
class Memorial(BasePicModel):
    __tablename__ = 'memorials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    creator = relationship("User", back_populates="memorials")
    users = relationship("MemorialUser", back_populates="memorial", cascade="all, delete-orphan")
    invited_keys = relationship("InviteKey", back_populates="memorial", cascade="all, delete-orphan")
    photos = relationship("MemorialPhoto", back_populates="memorial", cascade="all, delete-orphan")
    deceased = relationship("Deceased", back_populates="memorial", cascade="all, delete-orphan")
    family_tree = relationship("FamilyTree", back_populates="memorial", cascade="all, delete-orphan")
    offerings = relationship("MemorialOffering", back_populates="memorial", cascade="all, delete-orphan")
    messages = relationship("MemorialMessage", back_populates="memorial", cascade="all, delete-orphan")
    special_offerings = relationship("SpecialOffering", back_populates="memorial", cascade="all, delete-orphan")

# MemorialUser Model (for invited users)
class MemorialUser(BaseModel):
    __tablename__ = 'memorial_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    # Relationships
    memorial = relationship("Memorial", back_populates="users")
    user = relationship("User", back_populates="memorial_user_links")

# InviteKey Model
class InviteKey(BaseModel):
    __tablename__ = 'invite_keys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'), nullable=False)
    key_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="invited_keys")
    memorial = relationship("Memorial", back_populates="invited_keys")

    def set_key(self, key):
        self.key_hash = generate_password_hash(key)

    def check_key(self, key):
        return check_password_hash(self.key_hash, key)

# MemorialPhoto Model
class MemorialPhoto(BasePicModel):
    __tablename__ = 'memorial_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'), nullable=False)
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'), nullable=False)
    description = Column(Text)
    photo_date = Column(Date)
    uploaded_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="photos")
    deceased = relationship("Deceased", back_populates="photos")

# Deceased Model
class Deceased(BasePicModel):
    __tablename__ = 'deceased'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    biography = Column(Text)

    # Relationships
    memorial = relationship("Memorial", back_populates="deceased")
    family1 = relationship("FamilyTree", foreign_keys="[FamilyTree.deceased1_id]", back_populates="deceased1")
    family2 = relationship("FamilyTree", foreign_keys="[FamilyTree.deceased2_id]", back_populates="deceased2")
    photos = relationship("MemorialPhoto", back_populates="deceased", cascade="all, delete-orphan")

# FamilyTree Model
class FamilyTree(BaseModel):
    __tablename__ = 'family_trees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'), nullable=False)
    deceased1_id = Column(Integer, ForeignKey('deceased.id', ondelete='SET NULL'), nullable=False)
    deceased2_id = Column(Integer, ForeignKey('deceased.id', ondelete='SET NULL'), nullable=False)
    relation_type = Column(String(50), nullable=False)

    # Relationships
    memorial = relationship("Memorial", back_populates="family_tree")
    deceased1 = relationship("Deceased", foreign_keys=[deceased1_id])
    deceased2 = relationship("Deceased", foreign_keys=[deceased2_id])

# Offering Model
class Offering(BasePicModel):
    __tablename__ = 'offerings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    special_offering = Column(Boolean, default=False)

    # Relationships
    user_offerings = relationship("UserOffering", back_populates="offering", cascade="all, delete-orphan")
    memorial_offerings = relationship("MemorialOffering", back_populates="offering", cascade="all, delete-orphan")
    special_offerings = relationship("SpecialOffering", back_populates="offering", cascade="all, delete-orphan")

# SpecialOffering Model
class SpecialOffering(BaseModel):
    __tablename__ = 'special_offerings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'))
    offering_id = Column(Integer, ForeignKey('offerings.id', ondelete='CASCADE'))
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="special_offerings")
    offering = relationship("Offering", back_populates="special_offerings")

# UserOffering Model
class UserOffering(BaseModel):
    __tablename__ = 'user_offerings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    offering_id = Column(Integer, ForeignKey('offerings.id', ondelete='CASCADE'))
    quantity = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="user_offerings")
    offering = relationship("Offering", back_populates="user_offerings")

# MemorialOffering Model
class MemorialOffering(BaseModel):
    __tablename__ = 'memorial_offerings'
    id = Column(Integer, ForeignKey('offerings.id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'))
    quantity = Column(Integer, default=0)
    offered_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    offering = relationship("Offering", back_populates="memorial_offerings")
    user = relationship("User", back_populates="memorial_offerings")
    memorial = relationship("Memorial", back_populates="offerings")

# MemorialMessage Model
class MemorialMessage(BaseModel):
    __tablename__ = 'memorial_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    posted_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="messages")
    user = relationship("User", back_populates="memorial_messages")

# RemembranceMessage Model
class RemembranceMessage(BaseModel):
    __tablename__ = 'remembrance_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    posted_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="remembrance_messages")

class DailyQuestion(BaseModel):
    __tablename__ = 'daily_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question=Column(Text, nullable=False)
    answerA=Column(Text, nullable=False)
    answerB = Column(Text, nullable=False)
    answerC = Column(Text, nullable=False)
    answerD = Column(Text, nullable=False)
    correctAnswer=Column(Text, nullable=False)
    explanation=Column(Text, nullable=False)

class TodayInHistory(BaseModel):
    __tablename__ = 'today_in_history'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)
    insert_time = db.Column(db.BigInteger, nullable=False)
