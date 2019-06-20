from enum import Enum

from university_system.models import department_info_manager, user_info_manager
from university_system.server import repsrep

repository = repsrep.get_repository('departments')


class DepartmentLevel(Enum):
    group = 'Group'
    chair = 'Faculty'
    university = 'University'


class Department:
    def __init__(self, info_id=None, parent_department_id=None, departments_id=[],
                 users_info_id=[], level=None):
        self.info_id = info_id
        self.parent_department_id = parent_department_id
        self.departments_id = departments_id
        self.users_info_id = users_info_id
        self.level = level


def bind_to_info(department_id, department_info_id):
    department = repository.get(department_id)
    department_info = department_info_manager.repository.get(department_info_id)
    department.info_id = department_info_id
    department_info.department_id = department_id
    repository.update(department)
    department_info_manager.repository.update(department_info)
    return department_id


def bind_to_user(user_info_id, department_id):
    department = repository.get(department_id)
    department.users_info_id.append(user_info_id)
    repository.update(department)
    if department.parent_department_id is not None:
        bind_to_user(user_info_id, department.parent_department_id)


def unbind_from_user(user_info_id, department_id):
    department = repository.get(department_id)
    department.users_id.remove(user_info_id)
    repository.update(department)
    if department.parent_departmant is not None:
        unbind_from_user(user_info_id, department_id)


def unbind_users(department_id):
    department = get(department_id)
    if department.users_info_id is not None:
        for user_info_id in department.users_info_id:
            user_info = user_info_manager.get(user_info_id)
            user_info.department_id = None
            user_info_manager.update(user_info)


def bind_departments(parent_department_id, child_department_id):
    parent_department = repository.get(parent_department_id)
    parent_department.departments_id.append(child_department_id)
    repository.update(parent_department)
    if parent_department.parent_department_id is not None:
        bind_departments(parent_department.parent_department_id, child_department_id)
    # child = repository.get(child_id)
    # child.parent_department_id = parent_id
    # repository.update(child)


def unbind_departments(parent_department_id, child_department_id):
    parent_department = repository.get(parent_department_id)
    parent_department.departments_id.remove(child_department_id)
    repository.update(parent_department)
    if parent_department.parent_department_id is not None:
        unbind_departments(parent_department.parent_department_id, child_department_id)


def add_and_bind(department, info):
    department_id = add(department)
    info_id = department_info_manager.add(info)
    return bind_to_info(department_id, info_id)


def add(department):
    return repository.add(department)


def update(new_department):
    repository.update(new_department)


def delete(department_id):
    repository.delete(department_id)


def delete_children(department_id):
    department = get(department_id)
    if department.departments_id is not None:
        for child_id in department.departments_id:
            delete_and_unbind(child_id)


def search(key, value=None, as_list=True):
    return repository.search(key, value, as_list)


def get(id):
    return repository.get(id)


def check(title):
    if search('title', title) is not None:
        return 'This title exists'
    return None


def delete_and_unbind(department_id):
    department = get(department_id)
    unbind_users(department_id)
    delete_children(department_id)
    unbind_departments(department.parent_department_id, department_id)
    delete(department_id)
