from collections.abc import Mapping

from university_system.auth import permissions
from university_system.models import user_manager, user_info_manager, department_info_manager, achievement_manager, \
    department_manager
from university_system.server import json_converter


# application = get_wsgi_application()


def to_form(obj, form, nested_obj=None, nested_form=None):
    if nested_obj is not None:
        for field in obj:
            if isinstance(obj[field], Mapping):
                obj.pop(field)
        return form(obj), nested_form(nested_obj)
    else:
        return form(obj)


def form_to_object(form, old_object):
    obj_dict = old_object if type(old_object) is json_converter.Wrapper else old_object.__dict__
    for key in obj_dict:
        value = form.cleaned_data.get(key)
        if value is not None and value != '':
            if key == 'date':
                obj_dict[key] = value.__str__()
            elif key == 'password':
                obj_dict[key] = user_manager.hash(value)
            elif 'id' in key and not isinstance(value, list) and not isinstance(value, Mapping):
                obj_dict[key] = int(value)
            else:
                obj_dict[key] = value
    return obj_dict if type(old_object) is json_converter.Wrapper else json_converter.Wrapper(obj_dict)


def get_without_enums(dirty_object):
    for key in dirty_object:
        value = dirty_object[key]
        if key == 'role':
            dirty_object[key] = permissions.from_str(permissions.Role, value).value
        elif key == 'type':
            dirty_object[key] = permissions.from_str(user_manager.Type, value).value
        elif key == 'sex':
            dirty_object[key] = permissions.from_str(user_info_manager.Sex, value).value
        elif key == 'level':
            dirty_object[key] = permissions.from_str(department_manager.DepartmentLevel, value).value
        elif key == 'category':
            dirty_object[key] = permissions.from_str(achievement_manager.Category, value).value
    return dirty_object
