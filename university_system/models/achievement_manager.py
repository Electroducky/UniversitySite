from enum import Enum

from university_system.auth.permissions import forDjango
from university_system.server import repsrep

repository = repsrep.get_repository('achievements')


@forDjango
class Category(Enum):
    social = 'Social'
    sport = 'Sport'
    education = 'Education'


class Achievement:
    def __init__(self, title=None, category=None, date=None, description=None, user_info_id=None):
        self.title = title
        self.category = category
        self.date = date
        self.description = description
        self.user_info_id = user_info_id


def add(achievement):
    return repository.add(achievement)


def update(achievement):
    repository.update(achievement)


def delete(achievement_id):
    repository.delete(achievement_id)


def search(key, value=None, as_list=True):
    return repository.search(key, value, as_list)


def get(id):
    return repository.get(id)
