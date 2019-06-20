from enum import Enum

from university_system.auth.permissions import forDjango
from university_system.models import achievement_manager, department_manager
from university_system.server import repsrep

repository = repsrep.get_repository('users_info')


@forDjango
class Sex(Enum):
    male = 'Male'
    female = 'Female'


class UserInfo:
    def __init__(self, sex=None, name=None, surname=None, patronymic=None, date=None, description=None, user_id=None):
        self.sex = sex
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.date = date
        self.description = description
        self.user_id = user_id


class StudentInfo(UserInfo):
    def __init__(self, sex=None, name=None, surname=None, patronymic=None, date=None, description=None,
                 achievements_id=[],
                 user_id=None, department_id=None):
        super().__init__(sex, name, surname, patronymic, date, description, user_id)
        self.achievements_id = achievements_id
        self.department_id = department_id


def add(user):
    return repository.add(user)


def update(user):
    repository.update(user)


def delete(user_id):
    repository.delete(user_id)


def search(key, value=None, as_list=True):
    return repository.search(key, value, as_list)


def get(id):
    return repository.get(id)


def bind_to_achievement(stuff, user_info_id, achievement_id):
    user_info = repository.get(user_info_id)
    achievement = achievement_manager.repository.get(achievement_id)
    user_info.achievements_id.append(achievement_id)
    achievement.user_info_id = user_info_id
    repository.update(user_info)
    achievement_manager.repository.update(achievement)
    return user_info_id, achievement_id


def unbind_from_achievement(user_info_id, achievement_id):
    user_info = get(user_info_id)
    print(user_info)
    user_info.achievements_id.remove(achievement_id)
    update(user_info)
    achievement = achievement_manager.get(achievement_id)
    print(achievement)
    achievement.user_info_id = None
    achievement_manager.update(achievement)


def unbind_from_department(user_info_id, department_id):
    department = department_manager.get(department_id)
    if department.parent_department_id is not None:
        unbind_from_department(user_info_id, department.parent_department_id )
    department.users_info_id.remove(user_info_id)
    department_manager.update(department)


def delete_and_unbind(user_info):
    if user_info.get('department_id') is not None:
        unbind_from_department(user_info.doc_id, user_info.department_id)
    if user_info.get('achievements_id') is not None and len(user_info.get('achievements_id')) != 0:
        for id in user_info.achievements_id:
            achievement_manager.delete(id)
    delete(user_info.doc_id)
