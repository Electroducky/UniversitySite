import hashlib

from university_system.models import user_info_manager
from university_system.server import repsrep

repository = repsrep.get_repository('users')

from enum import Enum

from university_system.auth.permissions import forDjango


@forDjango
class Type(Enum):
    person = 'Person'
    student = 'Student'
    admin = 'Admin'


class User:
    def __init__(self, login=None, password=None, role=None, type=None, info_id=None):
        self.login = login
        self.password = hash(password) if password is not None else None
        self.role = role
        self.type = type
        self.info_id = info_id


def add_and_bind(user, info):
    user_id = add(user)
    info_id = user_info_manager.add(info)
    return bind_to_info(user_id, info_id)


def add(user):
    return repository.add(user)


def update(user):
    repository.update(user)


def delete(user_id):
    repository.delete(user_id)


def check(login, password, is_user_created=True):
    if is_user_created:
        if search('login', login) is None:
            return 'Login is incorrect'
        if search('password', hash(password)) is None:
            return 'Password is incorrect'
    else:
        if search('login', login) is not None:
            return 'This login exists'
    return None


def bind_to_info(user_id, info_id):
    user = repository.get(user_id)
    info = user_info_manager.repository.get(info_id)
    user.info_id = info_id
    info.user_id = user_id
    repository.update(user)
    user_info_manager.repository.update(info)
    return user_id, info_id


def get(id):
    return repository.get(id)


def search(key, value=None, as_list=True):
    return repository.search(key, value, as_list)


def hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
