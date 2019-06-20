from university_system.server import repsrep

repository = repsrep.get_repository('departments_info')


class DepartmentInfo:
    def __init__(self, title=None, date=None, description=None, head=None, department_id=None):
        self.title = title
        self.date = date
        self.description = description
        self.head = head
        self.department_id = department_id


class Head:
    def __init__(self, name=None, surname=None, patronymic=None, date=None):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.date = date


def add(department_info):
    return repository.add(department_info)


def update(department_info):
    repository.update(department_info)


def delete(department_info_id):
    repository.delete(department_info_id)


def search(key, value=None, as_list=True):
    return repository.search(key, value, as_list)


def get(id):
    return repository.get(id)


def fill_attribute(id, field_name, value, as_list=False):
    info = get(id)
    if as_list:
        info[field_name].append(value)
    else:
        info[field_name] = value
    update(info)


