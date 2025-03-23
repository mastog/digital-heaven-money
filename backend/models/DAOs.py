import os
from typing import TypeVar, Type

from backend import app
from backend.models.models import *

ModelType = TypeVar('ModelType')

class BaseDAO:
    def __init__(self, model: Type[ModelType]):
        self.session = db.session
        self.model = model

    def _filter_valid_fields(self, data: dict) -> dict:
        #Filter out fields that do not exist in the model
        model_columns = inspect(self.model).columns.keys()
        if "_pic_url" in model_columns:
            model_columns.append("pic_url")
        return {key: value for key, value in data.items() if key in model_columns}

    # create
    def create(self, **data) -> ModelType:
        filtered_data = self._filter_valid_fields(data)
        instance = self.model(**filtered_data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    # update
    def update(self, instance: ModelType, **data) -> ModelType:
        filtered_data = self._filter_valid_fields(data)
        if 'pic_url' in filtered_data and filtered_data['pic_url']!=getattr(instance, 'pic_url', ''):
            # pic_url is not empty and has been changed
            delete_pic(instance)
        for key, value in filtered_data.items():
            setattr(instance, key, value)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    # delete
    def delete(self, instance: ModelType) -> None:
        delete_pic(instance)
        self.session.delete(instance)
        self.session.commit()

    # get single
    def get(self, **filters) -> ModelType:
        return self.session.query(self.model).filter_by(**filters).first()

    # get all
    def get_all(self, **filters) -> list[ModelType]:
        return self.session.query(self.model).filter_by(**filters).all()

# delete the updated pictures
def delete_pic(instance):
    if hasattr(instance, 'pic_url') and instance.pic_url:
        file_path = os.path.join(app.config['FILE_UPLOAD_DIR'], instance.pic_url.replace("/uploaded_Pic/", ""))
        if os.path.exists(file_path):
            # delete file
            os.remove(file_path)

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

class DailyQuestionDAO(BaseDAO):
    def __init__(self):
        super().__init__(DailyQuestion)

class HistoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(TodayInHistory)

class DAOFactory:
    def __init__(self):
        # Initialize all DAO instances
        self.dao_map = {
            "User": UserDAO(),
            "Memorial": MemorialDAO(),
            "MemorialUser": MemorialUserDAO(),
            "InviteKey": InviteKeyDAO(),
            "MemorialPhoto": MemorialPhotoDAO(),
            "Deceased": DeceasedDAO(),
            "FamilyTree": FamilyTreeDAO(),
            "Offering": OfferingDAO(),
            "SpecialOffering": SpecialOfferingDAO(),
            "UserOffering": UserOfferingDAO(),
            "MemorialOffering": MemorialOfferingDAO(),
            "MemorialMessage": MemorialMessageDAO(),
            "RemembranceMessage": RemembranceMessageDAO(),
            "DailyQuestion": DailyQuestionDAO(),
            "History": HistoryDAO()
        }

    def get_dao(self, name: str) -> BaseDAO | None:
        # Return the corresponding DAO instance by name
        return self.dao_map.get(name, None)

dao_factory = DAOFactory()