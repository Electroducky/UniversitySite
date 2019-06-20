from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views import View

from university_system.auth import permissions, auth_user_manager
from university_system.forms import form_converter
from university_system.forms.achievement_form import AchievementForm
from university_system.models import user_info_manager, achievement_manager, department_manager, department_info_manager
from university_system.views import base_views


class AchievementCreate(base_views.ObjectCreate):
    form = AchievementForm
    model = achievement_manager.Achievement()
    template = "university_system/achievements/create.html"
    manager = achievement_manager
    scope = permissions.Scope.achievement
    is_bound_object = True
    bound_function = user_info_manager.bind_to_achievement
    text = 'The achievement was created'


class AchievementUpdate(base_views.ObjectUpdate):
    form = AchievementForm
    model = achievement_manager.Achievement()
    template = "university_system/achievements/update.html"
    manager = achievement_manager
    scope = permissions.Scope.achievement
    text = 'The achievement was updated'


class AchievementDelete(View):
    def post(self, request, id):
        auth_user = auth_user_manager.get(request.session.get('token', None))
        if auth_user is not None and auth_user.has_permission(permissions.Scope.achievement,
                                                              permissions.Crud.read):
            achievement = achievement_manager.get(id)
            user_info_manager.unbind_from_achievement(achievement.user_info_id, id)
            achievement_manager.delete(id)
            return base_views.home(request, 'The achievement was deleted')
        else:
            raise PermissionDenied


def achievements_by(request, template, scope=permissions.Scope.achievement, department_info_id=None, user_info_id=None):
    auth_user = auth_user_manager.get(request.session.get('token', None))
    if auth_user is not None and auth_user.has_permission(scope,
                                                          permissions.Crud.read):
        dirty_achievements = []
        clean_achievements = []
        user_info = None
        department_info = None
        if department_info_id is not None:
            department_info = department_info_manager.get(department_info_id)
            department = department_manager.get(department_info.department_id)
            for user_info_id in department.users_info_id:
                user_achievements = achievement_manager.search('user_info_id', user_info_id)
                if user_achievements is not None:
                    dirty_achievements.extend(achievement_manager.search('user_info_id', user_info_id))

        else:
            if user_info_id is None:
                user_info_id = auth_user.info_id
            user_info = user_info_manager.get(user_info_id)
            user_achievements = achievement_manager.search('user_info_id', user_info_id)
            if user_achievements is not None:
                dirty_achievements.extend(user_achievements)

        for achievement in dirty_achievements:
            clean_achievements.append(form_converter.get_without_enums(achievement))

        return render(request, template,
                      context={'achievements': clean_achievements, 'auth_user': auth_user, 'user_info': user_info,
                               'department_info': department_info})
    else:
        raise PermissionDenied


def chair_achievements(request, id):
    return achievements_by(request=request, template='university_system/achievements/chair_achievements.html',
                           department_info_id=id)


def group_achievements(request, id):
    return achievements_by(request=request, template='university_system/achievements/group_achievements.html',
                           department_info_id=id)


def student_achievements(request, id):
    return achievements_by(request=request, template='university_system/achievements/student_achievements.html',
                           user_info_id=id)


def my_achievements(request):
    return achievements_by(request=request, template='university_system/achievements/my_achievements.html',
                           scope=permissions.Scope.self)


def achievement_profile(request, id):
    auth_user = auth_user_manager.get(request.session.get('token', None))
    if auth_user is not None and auth_user.has_permission(permissions.Scope.achievement,
                                                          permissions.Crud.read):
        achievement = form_converter.get_without_enums(achievement_manager.get(id))
        user_info = user_info_manager.get(achievement.user_info_id)
        return render(request, "university_system/achievements/profile.html",
                      context={'achievement': achievement, 'auth_user': auth_user, 'user_info': user_info})
    else:
        raise PermissionDenied


def achievements(request):
    return achievements_by(request=request, template='university_system/achievements/list.html',
                           department_info_id=1)
