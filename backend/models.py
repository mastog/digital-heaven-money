from flask_sqlalchemy import SQLAlchemy

from backend import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Date, Table, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


# User Model
class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    photo_url = Column(String(255))
    is_admin = Column(Boolean, default=False)

    # Relationships
    memorials = relationship("Memorial", back_populates="creator", cascade="all, delete-orphan")
    memorial_user_links = relationship("MemorialUser", back_populates="user", cascade="all, delete-orphan")
    invited_keys = relationship("InviteKey", back_populates="user", cascade="all, delete-orphan")
    photos = relationship("MemorialPhoto", back_populates="user", cascade="all, delete-orphan")
    deceased = relationship("Deceased", back_populates="memorial", cascade="all, delete-orphan")
    user_offerings = relationship("UserOffering", back_populates="user", cascade="all, delete-orphan")
    memorial_offerings = relationship("MemorialOffering", back_populates="user", cascade="all, delete-orphan")
    memorial_messages = relationship("MemorialMessage", back_populates="user", cascade="all, delete-orphan")
    remembrance_messages = relationship("RemembranceMessage", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Memorial Model
class Memorial(db.Model):
    __tablename__ = 'memorials'
    memorial_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    photo_url = Column(String(255))
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
class MemorialUser(db.Model):
    __tablename__ = 'memorial_users'
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    memorial = relationship("Memorial", back_populates="users")
    user = relationship("User", back_populates="memorial_user_links")

# InviteKey Model
class InviteKey(db.Model):
    __tablename__ = 'invite_keys'
    key_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), nullable=False)
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
class MemorialPhoto(db.Model):
    __tablename__ = 'memorial_photos'
    photo_id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    photo_url = Column(String(255), nullable=False)
    description = Column(Text)
    photo_date = Column(Date)
    uploaded_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="photos")
    user = relationship("User", back_populates="photos")

# Deceased Model
class Deceased(db.Model):
    __tablename__ = 'deceased'
    deceased_id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    biography = Column(Text)
    photo_url = Column(String(255))

    # Relationships
    memorial = relationship("Memorial", back_populates="deceased")
    family = relationship("FamilyTree", back_populates="deceased")

# FamilyTree Model
class FamilyTree(db.Model):
    __tablename__ = 'family_trees'
    relation_id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), nullable=False)
    deceased1_id = Column(Integer, ForeignKey('deceased.deceased_id', ondelete='SET NULL'), nullable=False)
    deceased2_id = Column(Integer, ForeignKey('deceased.deceased_id', ondelete='SET NULL'), nullable=False)
    relation_type = Column(String(50), nullable=False)

    # Relationships
    memorial = relationship("Memorial", back_populates="family_tree")
    deceased1 = relationship("Deceased", foreign_keys=[deceased1_id])
    deceased2 = relationship("Deceased", foreign_keys=[deceased2_id])

# Offering Model
class Offering(db.Model):
    __tablename__ = 'offerings'
    offering_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(String(255))
    special_offering = Column(Boolean, default=False)

    # Relationships
    user_offerings = relationship("UserOffering", back_populates="offering", cascade="all, delete-orphan")
    memorial_offerings = relationship("MemorialOffering", back_populates="offering", cascade="all, delete-orphan")
    special_offerings = relationship("SpecialOffering", back_populates="offering", cascade="all, delete-orphan")

# SpecialOffering Model
class SpecialOffering(db.Model):
    __tablename__ = 'special_offerings'
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), primary_key=True)
    offering_id = Column(Integer, ForeignKey('offerings.offering_id', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="special_offerings")
    offering = relationship("Offering", back_populates="special_offerings")

# UserOffering Model
class UserOffering(db.Model):
    __tablename__ = 'user_offerings'
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    offering_id = Column(Integer, ForeignKey('offerings.offering_id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="user_offerings")
    offering = relationship("Offering", back_populates="user_offerings")

# MemorialOffering Model
class MemorialOffering(db.Model):
    __tablename__ = 'memorial_offerings'
    offering_id = Column(Integer, ForeignKey('offerings.offering_id', ondelete='CASCADE'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), primary_key=True)
    quantity = Column(Integer, default=0)
    offered_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    offering = relationship("Offering", back_populates="memorial_offerings")
    user = relationship("User", back_populates="memorial_offerings")
    memorial = relationship("Memorial", back_populates="offerings")

# MemorialMessage Model
class MemorialMessage(db.Model):
    __tablename__ = 'memorial_messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    memorial_id = Column(Integer, ForeignKey('memorials.memorial_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    posted_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    memorial = relationship("Memorial", back_populates="messages")
    user = relationship("User", back_populates="memorial_messages")

# RemembranceMessage Model
class RemembranceMessage(db.Model):
    __tablename__ = 'remembrance_messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    posted_at = Column(DateTime, server_default=db.func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="remembrance_messages")
