from datetime import datetime, date

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from backend import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Date, Table, UniqueConstraint, \
    PrimaryKeyConstraint, inspect
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from backend.services.utils import allowed_file


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        columns = inspect(self.__class__).columns.keys()
        if "_pic_url" in columns:
            columns.remove("_pic_url")
            columns.append("pic_url")
        result = {}
        for column in columns:
            value = getattr(self, column)
            if value:
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
        if allowed_file(value):
            if value and not value.startswith("/uploaded_Pic/"):
                self._pic_url = f"/uploaded_Pic/{value}"
            else:
                self._pic_url = value


# User Model
class User(BasePicModel, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    gender = Column(String(100))
    location = Column(String(100))
    introduction = Column(Text)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    deceaseds = relationship("Deceased", back_populates="creator", cascade="all, delete-orphan")
    deceased_user_links = relationship("DeceasedUser", back_populates="user", cascade="all, delete-orphan")
    invited_keys = relationship("InviteKey", back_populates="user", cascade="all, delete-orphan")
    deceased_offerings = relationship("DeceasedOffering", back_populates="user", cascade="all, delete-orphan")
    deceased_messages = relationship("DeceasedMessage", back_populates="user", cascade="all, delete-orphan")
    family_trees = relationship("FamilyTree", back_populates="creator", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Deceased Model (merged with Memorial)
class Deceased(BasePicModel):
    __tablename__ = 'deceased'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    birth_date = Column(Text)
    death_date = Column(Text)
    biography = Column(Text)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    creator = relationship("User", back_populates="deceaseds")
    users = relationship("DeceasedUser", back_populates="deceased", cascade="all, delete-orphan")
    invited_keys = relationship("InviteKey", back_populates="deceased", cascade="all, delete-orphan")
    photos = relationship("DeceasedPhoto", back_populates="deceased", cascade="all, delete-orphan")
    family1 = relationship("FamilyTree", foreign_keys="[FamilyTree.deceased1_id]", back_populates="deceased1")
    family2 = relationship("FamilyTree", foreign_keys="[FamilyTree.deceased2_id]", back_populates="deceased2")
    offerings = relationship("DeceasedOffering", back_populates="deceased", cascade="all, delete-orphan")
    messages = relationship("DeceasedMessage", back_populates="deceased", cascade="all, delete-orphan")

# DeceasedUser Model (for invited users)
class DeceasedUser(BaseModel):
    __tablename__ = 'deceased_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    # Relationships
    deceased = relationship("Deceased", back_populates="users")
    user = relationship("User", back_populates="deceased_user_links")

# InviteKey Model
class InviteKey(BaseModel):
    __tablename__ = 'invite_keys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'), nullable=False)
    key_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="invited_keys")
    deceased = relationship("Deceased", back_populates="invited_keys")

    def set_key(self, key):
        self.key_hash = generate_password_hash(key)

    def check_key(self, key):
        return check_password_hash(self.key_hash, key)

# DeceasedPhoto Model (previously MemorialPhoto)
class DeceasedPhoto(BasePicModel):
    __tablename__ = 'deceased_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'), nullable=False)
    title = Column(Text)
    description = Column(Text)
    photo_date = Column(Text)
    uploaded_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    deceased = relationship("Deceased", back_populates="photos")

# FamilyTree Model
class FamilyTree(BaseModel):
    __tablename__ = 'family_trees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deceased1_id = Column(Integer, ForeignKey('deceased.id', ondelete='SET NULL'), nullable=False)
    deceased2_id = Column(Integer, ForeignKey('deceased.id', ondelete='SET NULL'), nullable=False)
    relation_type = Column(String(50), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # 新增creator_id字段

    # Relationships
    deceased1 = relationship("Deceased", foreign_keys=[deceased1_id])
    deceased2 = relationship("Deceased", foreign_keys=[deceased2_id])
    creator = relationship("User", back_populates="family_trees")  # 新增relationship到User

# Offering Model
class Offering(BasePicModel):
    __tablename__ = 'offerings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # Relationships
    deceased_offerings = relationship("DeceasedOffering", back_populates="offering", cascade="all, delete-orphan")


# DeceasedOffering Model (previously MemorialOffering)
class DeceasedOffering(BaseModel):
    __tablename__ = 'deceased_offerings'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Changed this to auto-increment
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'))
    offering_id = Column(Integer, ForeignKey('offerings.id', ondelete='CASCADE'))
    quantity = Column(Integer, default=1)
    offered_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    offering = relationship("Offering", back_populates="deceased_offerings", foreign_keys=[offering_id])
    user = relationship("User", back_populates="deceased_offerings")
    deceased = relationship("Deceased", back_populates="offerings")

# DeceasedMessage Model (previously MemorialMessage)
class DeceasedMessage(BaseModel):
    __tablename__ = 'deceased_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    deceased_id = Column(Integer, ForeignKey('deceased.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    posted_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    deceased = relationship("Deceased", back_populates="messages")
    user = relationship("User", back_populates="deceased_messages")


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