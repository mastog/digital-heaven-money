from sqlalchemy.orm import Session
from typing import TypeVar, Type

from werkzeug.security import generate_password_hash

from backend.models import *

ModelType = TypeVar('ModelType')

class BaseDAO:
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
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
    def __init__(self, session: Session):
        super().__init__(session, User)

    def create(self, **data):
        # hash the password
        password = data.pop('password', None)
        if password:
            data['password_hash'] = generate_password_hash(password)
        return super().create(**data)

class MemorialDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Memorial)

class MemorialUserDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, MemorialUser)

class InviteKeyDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, InviteKey)

    def create(self, **data):
        # hash key
        key = data.pop('key', None)
        if key:
            data['key_hash'] = generate_password_hash(key)
        return super().create(**data)

class MemorialPhotoDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, MemorialPhoto)

class DeceasedDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Deceased)

class FamilyTreeDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, FamilyTree)

class OfferingDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Offering)

class SpecialOfferingDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, SpecialOffering)

class UserOfferingDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, UserOffering)

class MemorialOfferingDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, MemorialOffering)

class MemorialMessageDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, MemorialMessage)

class RemembranceMessageDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, RemembranceMessage)

