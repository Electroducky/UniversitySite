from django import template

from university_system.auth import permissions, auth_user_manager
from university_system.models import department_manager, department_info_manager, user_info_manager

register = template.Library()


@register.filter(name='has_permission')
def has_permission(token, args):
    user = auth_user_manager.get(token)
    args_list = [arg.strip() for arg in args.split(', ')]
    scope = permissions.from_str(permissions.Scope, args_list[0])
    permission = permissions.from_str(permissions.Crud, args_list[1])
    return user.permissions.has_permission(scope, permission)


@register.filter(name='department_title')
def department_title(id):
    department = department_manager.get(id)
    info = department_info_manager.get(department.info_id)
    return info.title


@register.filter
def parent_department_title(id):
    department = department_manager.get(id)
    parent = department_manager.get(department.parent_department_id)
    parent_info = department_info_manager.get(parent.info_id)
    return parent_info.title


@register.filter
def user_name(id):
    user_info = user_info_manager.get(id)
    return user_info.name


@register.filter
def user_surname(id):
    user_info = user_info_manager.get(id)
    return user_info.surname


@register.filter
def department_title_by_user(id):
    user_info = user_info_manager.get(id)
    return department_title(user_info.department_id)


@register.filter
def parent_department_title_by_user(id):
    user_info = user_info_manager.get(id)
    return parent_department_title(user_info.department_id)


@register.filter
def department_id_by_user(id):
    user_info = user_info_manager.get(id)
    department = department_manager.get(user_info.department_id)
    return department.info_id


@register.filter
def parent_department_id_by_user(id):
    user_info = user_info_manager.get(id)
    department = department_manager.get(user_info.department_id)
    parent = department_manager.get(department.parent_department_id)
    return parent.info_id
