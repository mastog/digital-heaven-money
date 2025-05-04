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


class DeceasedUserDAO(BaseDAO):
    def __init__(self):
        super().__init__(DeceasedUser)

class InviteKeyDAO(BaseDAO):
    def __init__(self):
        super().__init__(InviteKey)

    def create(self, **data):
        # hash key
        key = data.pop('key', None)
        if key:
            data['key_hash'] = generate_password_hash(key)
        return super().create(**data)

    def get(self, **filters) -> ModelType:
        key = filters.pop('key', None)
        if key:
            filters['key_hash']= generate_password_hash(key)
        return super().get(**filters)

class DeceasedPhotoDAO(BaseDAO):
    def __init__(self):
        super().__init__(DeceasedPhoto)

class DeceasedDAO(BaseDAO):
    def __init__(self):
        super().__init__(Deceased)


class FamilyTreeDAO(BaseDAO):
    def __init__(self):
        super().__init__(FamilyTree)

    def get_all(self, **filters) -> list[ModelType]:
        # If filters include deceased_id, we search for it in either deceased1_id or deceased2_id
        deceased_id = filters.get('deceased_id')
        if deceased_id:
            return self.session.query(self.model).filter(
                (self.model.deceased1_id == deceased_id) | (self.model.deceased2_id == deceased_id)
            ).all()
        return super().get_all(**filters)

    def create(self, **data):
        deceased1_id = data.get('deceased1_id')
        deceased2_id = data.get('deceased2_id')

        if deceased1_id and deceased2_id:
            # Check if a family tree entry already exists with these deceased IDs
            existing_family_tree = self.session.query(self.model).filter(
                (self.model.deceased1_id == deceased1_id) & (self.model.deceased2_id == deceased2_id) |
                (self.model.deceased1_id == deceased2_id) & (self.model.deceased2_id == deceased1_id)
            ).first()

            if existing_family_tree:
                # If it exists, update the relation_type
                existing_family_tree.relation_type = data.get('relation_type', existing_family_tree.relation_type)
                self.session.commit()
                self.session.refresh(existing_family_tree)
                return existing_family_tree

        # If no existing entry, create a new one
        return super().create(**data)

class OfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(Offering)

class DeceasedOfferingDAO(BaseDAO):
    def __init__(self):
        super().__init__(DeceasedOffering)

    def create(self, **data):
        instance = self.get(**data)
        if instance:
            if hasattr(instance, 'quantity') and isinstance(instance.quantity, int):
                instance.quantity += 1
            else:
                instance.quantity = 1  # fallback
            self.session.commit()
            self.session.refresh(instance)
            return instance
        else:
            return super().create(**data)

class DeceasedMessageDAO(BaseDAO):
    def __init__(self):
        super().__init__(DeceasedMessage)

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
            "DeceasedUser": DeceasedUserDAO(),
            "InviteKey": InviteKeyDAO(),
            "DeceasedPhoto": DeceasedPhotoDAO(),
            "Deceased": DeceasedDAO(),
            "FamilyTree": FamilyTreeDAO(),
            "Offering": OfferingDAO(),
            "DeceasedOffering": DeceasedOfferingDAO(),
            "DeceasedMessage": DeceasedMessageDAO(),
            "DailyQuestion": DailyQuestionDAO(),
            "History": HistoryDAO()
        }

    def get_dao(self, name: str) -> BaseDAO | None:
        # Return the corresponding DAO instance by name
        return self.dao_map.get(name, None)

    def get_dao_keys(self) -> list[str]:
        return list(self.dao_map.keys())

dao_factory = DAOFactory()