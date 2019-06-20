from enum import Enum


# def str_to_enum(enum_str):
#     return eval(enum_str)

def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls


def from_str(enum, enum_str):
    name, member = enum_str.split(".")
    return enum[member]


def get_value(enum_obj):
    return enum_obj.value


class Permissions:
    def __init__(self, permissions_dict=None):
        if permissions_dict is None:
            permissions_dict = {}
        self.permissions = permissions_dict

    def add_permission(self, scope, permission):
        if isinstance(permission, list):
            self.permissions[scope].extend(permission)
        else:
            self.permissions[scope].append(permission)

    def has_permission(self, scope, permission):
        return permission in self.permissions[scope]


@forDjango
class Scope(Enum):
    self = 10
    student = 20
    admin = 30
    department = 40
    achievement = 50


@forDjango
class Crud(Enum):
    create = 10
    read = 20
    update = 30
    delete = 40


@forDjango
class Role(Enum):
    student = 'Student'
    admin = 'Admin'

    def get_scope(self):
        if self == Role.student:
            return Scope.student
        if self == Role.admin:
            return Scope.admin

    def get_permissions(self):
        if self == Role.student:
            return Permissions(student_permissions_dict)
        if self == Role.admin:
            return Permissions(admin_permissions_dict)


student_permissions_dict = {
    Scope.self: [Crud.read, Crud.update],
    Scope.student: [Crud.read],
    Scope.admin: [],
    Scope.department: [Crud.read],
    Scope.achievement: [Crud.create, Crud.read]
}

admin_permissions_dict = {
    Scope.self: [Crud.read, Crud.update],
    Scope.student: [Crud.read, Crud.update, Crud.create,
                    Crud.delete],
    Scope.admin: [Crud.read],
    Scope.department: [Crud.read, Crud.update, Crud.create,
                       Crud.delete],
    Scope.achievement: [Crud.read, Crud.update, Crud.delete]
}

print(Role.student.value)
