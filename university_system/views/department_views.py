from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View

from university_system.auth import auth_user_manager, permissions
from university_system.forms.department_forms import *
from university_system.forms.form_converter import form_to_object
from university_system.models import department_manager, department_info_manager
from university_system.views import base_views


def departments_by(request, level, id=None, template=None):
    auth_user = auth_user_manager.get(request.session.get('token', None))
    if auth_user is not None and auth_user.has_permission(permissions.Scope.department,
                                                          permissions.Crud.read):
        departments = department_manager.search('level', level) if id is None else department_manager.search(
            ['level', 'parent_department_id'], [level, id])
        clean_departments_info = []
        for department in departments:
            clean_departments_info.append(department_info_manager.get(department.info_id))
        return render(request, template,
                      context={"departments": departments, 'departments_info': clean_departments_info,
                               'auth_user': auth_user})
    else:
        raise PermissionDenied


def faculties(request):
    return departments_by(request, 'DepartmentLevel.chair', id=1,
                          template='university_system/departments/faculties.html')


def groups(request):
    return departments_by(request, 'DepartmentLevel.group', template='university_system/departments/groups.html')


def faculty_groups(request, id):
    return departments_by(request, 'DepartmentLevel.group', id, 'university_system/departments/groups.html')


class DepartmentCreate(View):
    def get(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(permissions.Scope.department,
                                                              permissions.Crud.create):
            form = DepartmentForm()
            template = "university_system/departments/create.html"
            info_form = DepartmentInfoForm()
            return render(request, template,
                          context={'form': form,
                                   'info_form': info_form})
        else:
            raise PermissionDenied

    def post(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        form = DepartmentForm(request.POST)
        info_form = DepartmentInfoForm(request.POST)
        if form.is_valid() and info_form.is_valid():
            check = department_manager.check(info_form.cleaned_data['title'])
            if check is None:
                department = form_to_object(form, department_manager.Department())
                department_info = form_to_object(info_form, department_info_manager.DepartmentInfo())
                department_id = department_manager.add_and_bind(department, department_info)
                department_manager.bind_departments(department.parent_department_id, department_id)
                return base_views.home(request, text='Department was created')
            else:
                return render(request, "university_system/departments/create.html",
                              context={'form': form,
                                       'info_form': info_form,
                                       'check': check})
        return render(request, "university_system/departments/create.html",
                      context={'form': form,
                               'info_form': info_form, 'auth_user': auth_user})


class DepartmentInfoUpdate(base_views.ObjectUpdate):
    form = DepartmentInfoForm
    model = department_info_manager.DepartmentInfo()
    scope = permissions.Scope.department
    template = "university_system/departments/update.html"
    manager = department_info_manager
    text = 'The department was deleted'


class DepartmentDelete(View):
    def post(self, request, id):
        department_info = department_info_manager.get(id)
        department_manager.delete_and_unbind(department_info.department_id)
        department_info_manager.delete(id)
        return base_views.home(request, 'The department was deleted')


class HeadCreate(base_views.ObjectCreate):
    form = HeadForm
    model = department_info_manager.Head()
    template = "university_system/departments/head/create.html"
    manager = department_info_manager
    scope = permissions.Scope.department
    crud = permissions.Crud.update
    is_nested_object = True
    field = 'head'
    text = 'The head was created'


class HeadUpdate(base_views.ObjectUpdate):
    form = HeadForm
    model = department_info_manager.Head()
    template = "university_system/departments/head/update.html"
    manager = department_info_manager
    scope = permissions.Scope.department
    crud = permissions.Crud.update
    is_nested_object = True
    field = 'head'
    text = 'The head was updated'


class HeadDelete(base_views.ObjectDelete):
    manager = department_info_manager
    scope = permissions.Scope.department
    crud = permissions.Crud.update
    is_nested_object = True
    field = 'head'
    text = 'The head was deleted'


def department_profile(request, id, template="university_system/departments/profile.html"):
    auth_user = auth_user_manager.get(request.session.get('token', None))
    if auth_user is not None and auth_user.has_permission(permissions.Scope.department,
                                                          permissions.Crud.read):
        department_info = department_info_manager.get(id)
        department = department_manager.get(department_info.department_id)
        return render(request, template,
                      {'department': department, 'department_info': department_info, 'auth_user': auth_user})
    else:
        raise PermissionDenied


def university_profile(request):
    return department_profile(request, id=1, template="university_system/departments/university_profile.html")


def faculty_profile(request, id):
    return department_profile(request, id=id, template="university_system/departments/faculty_profile.html")

def group_profile(request, id):
    return department_profile(request, id=id, template="university_system/departments/group_profile.html")