from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View

from university_system.auth import auth_user_manager, permissions
from university_system.forms.form_converter import form_to_object, to_form
from university_system.models import department_info_manager


class ObjectCreate(View):
    form = None
    model = None
    template = None
    manager = None
    scope = None
    crud = permissions.Crud.create
    is_bound_object = None
    bound_function = None
    is_nested_object = False
    field = None
    text = None

    def get(self, request, id=None):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(self.scope,
                                                              self.crud):
            form = self.form
            return render(request, self.template, context={'form': form, 'id': id, 'auth_user': auth_user})
        else:
            raise PermissionDenied

    def post(self, request, id=None):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        form = self.form(request.POST)
        if form.is_valid():
            obj = form_to_object(form, self.model)
            if self.is_nested_object:
                self.manager.fill_attribute(id, self.field, obj)
            object_id = self.manager.add(obj)
            if self.is_bound_object:
                if id is None:
                    id = auth_user_manager.get(request.session.get('token')).info_id
                self.bound_function(id, object_id)
            return home(request, self.text)
        return render(request, self.template, context={'form': form, 'id': id, 'auth_user': auth_user})


class ObjectUpdate(View):
    form = None
    model = None
    template = None
    manager = None
    scope = None
    is_nested_object = False
    field = None
    text = None

    def get(self, request, id):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(self.scope,
                                                              permissions.Crud.update):
            object = self.manager.get(id)
            if self.is_nested_object:
                object = object[self.field]
            form = to_form(object, self.form)

            return render(request, self.template, context={
                'form': form, 'id': id, 'auth_user': auth_user})
        else:
            raise PermissionDenied

    def post(self, request, id):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        filled_form = self.form(request.POST)
        if filled_form.is_valid():
            old_object = self.manager.get(id)
            if self.is_nested_object:
                new_field = form_to_object(filled_form, self.model)
                old_object[self.field] = new_field
                new_object = old_object
            else:
                new_object = form_to_object(filled_form, old_object)
            self.manager.update(new_object)
            return home(request, self.text)
        return render(request, self.template, context={
            'form': filled_form, 'id': id, 'auth_user': auth_user})


class ObjectDelete(View):
    template = None
    manager = None
    scope = None
    crud = None
    is_nested_object = False
    field = None
    text = None

    def post(self, request, id):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(self.scope,
                                                              self.crud):
            object = self.manager.get(id)
            if self.is_nested_object:
                object[self.field] = None
                self.manager.update(object)

            return home(request, self.text)
        else:
            raise PermissionDenied


def home(request, text=None):
    auth_user = auth_user_manager.get(request.session.get('token', None))
    if auth_user is not None:
        department_info = department_info_manager.get(1)
        return render(request, "university_system/home.html",
                      context={'department_info': department_info, 'auth_user': auth_user, 'text': text})
