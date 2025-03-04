from sqlalchemy.orm import Session
from typing import TypeVar, Type

from backend.models import *

ModelType = TypeVar('ModelType')

class BaseDAO:
    def __init__(self, model: Type[ModelType]):
        self.session = db.session
        self.model = model

    # create
    def create(self, **data) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    # update
    def update(self, instance: ModelType, **data) -> ModelType:
        for key, value in data.items():
            setattr(instance, key, value)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    # delete
    def delete(self, instance: ModelType) -> None:
        self.session.delete(instance)
        self.session.commit()

    # get single
    def get(self, **filters) -> ModelType:
        return self.session.query(self.model).filter_by(**filters).first()

    # get all
    def get_all(self, **filters) -> list[ModelType]:
        return self.session.query(self.model).filter_by(**filters).all()

class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    def create(self, **data):
        # hash the password
        password = data.pop('password', None)
        if password:
            data['password_hash'] = generate_password_hash(password)
        return super().create(**data)

class MemorialDAO(BaseDAO):
    def __init__(self):
        super().__init__(Memorial)

class MemorialUserDAO(BaseDAO):
    def __init__(self):
        super().__init__(MemorialUser)

class InviteKeyDAO(BaseDAO):
    def __init__(self):
        super().__init__(InviteKey)

    def create(self, **data):
        # hash key
        key = data.pop('key', None)
        if key:
            data['key_hash'] = generate_password_hash(key)
        return super().create(**data)

class MemorialPhotoDAO(BaseDAO):
    def __init__(self):
        super().__init__(MemorialPhoto)

class DeceasedDAO(BaseDAO):
    def __init__(self):
        super().__init__(Deceased)

class FamilyTreeDAO(BaseDAO):
    def __init__(self):
        super().__init__(FamilyTree)

class OfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(Offering)

class SpecialOfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(SpecialOffering)

class UserOfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(UserOffering)

class MemorialOfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(MemorialOffering)

class MemorialMessageDAO(BaseDAO):
    def __init__(self):
        super().__init__(MemorialMessage)

class RemembranceMessageDAO(BaseDAO):
    def __init__(self):
        super().__init__(RemembranceMessage)


user_dao = UserDAO()
memorial_dao = MemorialDAO()
memorial_user_dao = MemorialUserDAO()
invite_key_dao = InviteKeyDAO()
memorial_photo_dao = MemorialPhotoDAO()
deceased_dao = DeceasedDAO()
family_tree_dao = FamilyTreeDAO()
offering_dao = OfferingDAO()
special_offering_dao = SpecialOfferingDAO()
user_offering_dao = UserOfferingDAO()
memorial_offering_dao = MemorialOfferingDAO()
memorial_message_dao = MemorialMessageDAO()
remembrance_message_dao = RemembranceMessageDAO()