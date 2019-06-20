from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View

from university_system.auth import auth_user_manager
from university_system.auth import permissions
from university_system.forms import form_converter
from university_system.forms.form_converter import to_form, form_to_object
from university_system.forms.user_forms import *
from university_system.models import user_info_manager, user_manager, department_manager, department_info_manager
from university_system.views import base_views


class UserCreate(View):
    form = None
    form_object = None
    info_form = None
    info_form_object = None
    model = None
    info_model = None
    template = None
    scope = None
    text = None

    def get(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(self.scope,
                                                              permissions.Crud.create):
            self.form_object.helper['type'].wrap(Field, type='hidden')
            self.form_object.helper['role'].wrap(Field, type='hidden')
            return render(request, self.template, context={'form': self.form_object,
                                                           'info_form': self.info_form_object, 'auth_user': auth_user})
        else:
            raise PermissionDenied

    def post(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        user_form = self.form(request.POST)
        user_info_form = self.info_form(request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            check = user_manager.check(user_form.cleaned_data['login'],
                                       user_form.cleaned_data['password'],
                                       False)
            if check is None:
                user = form_to_object(user_form, self.model)
                user_info = form_to_object(user_info_form, self.info_model)
                user_id, user_info_id = user_manager.add_and_bind(user, user_info)
                if user_info.get('department_id') is not None:
                    department_manager.bind_to_user(user_info_id, user_info.department_id)
                return base_views.home(request, self.text)
            else:
                return render(request, self.template, context={'form': self.form_object,
                                                               'info_form': self.info_form_object,
                                                               'check': check, 'auth_user': auth_user})
        return render(request, self.template, context={'form': self.form_object,
                                                       'info_form': self.info_form_object, 'auth_user': auth_user})


class UserDelete(View):
    def post(self, request, id):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(permissions.Scope.student,
                                                              permissions.Crud.delete):
            user_info = user_info_manager.get(id)
            user_info_manager.delete_and_unbind(user_info)
            user_manager.delete(user_info.user_id)
            return base_views.home(request, 'The user was deleted.')
        else:
            raise PermissionDenied


class ProfileUpdate(View):
    def get(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(permissions.Scope.self,
                                                              permissions.Crud.update):
            user_info = user_info_manager.get(auth_user.info_id)
            info_form = to_form(user_info, UserInfoForm)
            user = user_manager.get(auth_user.doc_id)
            form = to_form(user, UserForm)
            form.helper['type'].wrap(Field, type='hidden')
            form.helper['role'].wrap(Field, type='hidden')

            return render(request,
                          "university_system/users/profile_update.html", context={
                    'info_form': info_form, 'form': form, 'auth_user': auth_user})
        else:
            raise PermissionDenied

    def post(self, request):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        info_form = UserInfoForm(request.POST)
        form = UserForm(request.POST)
        if info_form.is_valid() and form.is_valid():
            old_user = user_manager.get(auth_user.doc_id)
            new_user = form_to_object(form, old_user)
            user_manager.update(new_user)
            old_user_info = user_info_manager.get(auth_user.info_id)
            new_user_info = form_to_object(info_form, old_user_info)
            user_info_manager.update(new_user_info)
            return base_views.home(request, 'Your profile was updated.')
        return render(request,
                      "university_system/users/profile_update.html", context={
                'info_form': info_form, 'form': form, 'auth_user': auth_user})


class StudentCreate(UserCreate):
    form = UserForm
    form_object = UserForm(initial={'role': 'Role.student', 'type': 'Type.student'})
    info_form = StudentInfoForm
    info_form_object = StudentInfoForm()
    model = user_manager.User()
    info_model = user_info_manager.StudentInfo()
    template = "university_system/users/students/create.html"
    scope = permissions.Scope.student
    text = 'The student was created'


class StudentUpdate(base_views.ObjectUpdate):
    form = StudentInfoForm
    model = user_info_manager.StudentInfo()
    template = "university_system/users/students/update.html"
    manager = user_info_manager
    scope = permissions.Scope.student
    text = 'The student was updated'


def my_profile(request):
    auth_user = auth_user_manager.get(request.session.get('token'))
    if auth_user is not None and auth_user.has_permission(permissions.Scope.self,
                                                          permissions.Crud.read):
        user = form_converter.get_without_enums(user_manager.get(auth_user.doc_id))
        user_info = form_converter.get_without_enums(user_info_manager.get(auth_user.info_id))
        return render(request, "university_system/users/profile.html",
                      context={"auth_user": auth_user, 'user': user,
                               'user_info': user_info})
    else:
        raise PermissionDenied


def users_by(request, scope=permissions.Scope.student, template="university_system/users/users.html", args=None):
    auth_user = auth_user_manager.get(request.session.get('token'))
    if auth_user is not None and auth_user.has_permission(scope,
                                                          permissions.Crud.read):
        if args is None:
            args = {'users_key': 'type',
                    'users_value': None,
                    'users_info_key': 'login',
                    'users_info_value': None}

        users = user_manager.search(args.get('users_key'), args.get('users_value'))
        users_info = []
        for user in users:
            users_info.append(user_info_manager.get(user.info_id))
        return render(request, template,
                      context={'users_info': users_info, 'auth_user': auth_user})
    else:
        raise PermissionDenied


def users_by_department(request, department_info_id, template, scope=permissions.Scope.student):
    auth_user = auth_user_manager.get(request.session.get('token'))
    if auth_user is not None and auth_user.has_permission(scope,
                                                          permissions.Crud.read):
        department_info = department_info_manager.get(department_info_id)
        department = department_manager.get(department_info.department_id)
        users_info = []
        for id in department.users_info_id:
            users_info.append(user_info_manager.get(id))

        return render(request, template,
                      context={'users_info': users_info, 'auth_user': auth_user})
    else:
        raise PermissionDenied


def user_profile(request, id, scope=permissions.Scope.student, template="university_system/users/profile.html"):
    auth_user = auth_user_manager.get(request.session.get('token'))
    if auth_user is not None and auth_user.has_permission(scope,
                                                          permissions.Crud.read):
        user_info = form_converter.get_without_enums(user_info_manager.get(id))
        user = form_converter.get_without_enums(user_manager.get(user_info.user_id))
        return render(request, template,
                      context={"user": user, 'user_info': user_info, 'auth_user': auth_user})
    else:
        raise PermissionDenied


def students(request):
    return users_by(request, args={'users_key': 'type',
                                   'users_value': 'Type.student'},
                    template="university_system/users/students/list.html")


def student_profile(request, id):
    return user_profile(request, id, template="university_system/users/profile.html")


def department_students(request, id):
    return users_by_department(request, id, "university_system/users/students/list.html")
