"""university_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from university_system.views import *
from university_system.views import user_views, department_views, auth_views, achievement_views, base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.Login.as_view(), name='default'),
    path('home', base_views.home, name='home'),
    path('login', auth_views.Login.as_view(), name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('university', department_views.university_profile, name='university-profile'),
    path('students', user_views.students, name='students'),
    path('profile', user_views.my_profile, name='profile'),
    path('profile/achievements', achievement_views.my_achievements, name='profile-achievements'),
    path('profile/update', user_views.ProfileUpdate.as_view(), name='profile-update'),
    path('students/<int:id>/profile', user_views.student_profile, name='students-profile'),
    path('students/create', user_views.StudentCreate.as_view(), name='students-create'),
    path('students/<int:id>/update', user_views.StudentUpdate.as_view(), name='students-update'),
    path('students/delete/<int:id>', user_views.UserDelete.as_view(), name='users-delete'),
    path('faculties', department_views.faculties, name='faculties'),
    path('departments/create', department_views.DepartmentCreate.as_view(), name='departments-create'),
    path('departments/<int:id>/update', department_views.DepartmentInfoUpdate.as_view(), name='departments-update'),
    path('departments/<int:id>/delete', department_views.DepartmentDelete.as_view(), name='departments-delete'),
    path('departments/<int:id>/head/create', department_views.HeadCreate.as_view(), name='head-create'),
    path('departments/<int:id>/head/update', department_views.HeadUpdate.as_view(), name='head-update'),
    path('departments/<int:id>/head/delete', department_views.HeadDelete.as_view(), name='head-delete'),
    path('achievements', achievement_views.achievements, name='achievements'),
    path('achievements/create', achievement_views.AchievementCreate.as_view(), name='achievements-create'),
    path('achievements/<int:id>/update', achievement_views.AchievementUpdate.as_view(), name='achievements-update'),
    path('achievements/<int:id>/delete', achievement_views.AchievementDelete.as_view(), name='achievements-delete'),
    path('achievements/<int:id>/profile', achievement_views.achievement_profile, name='achievements-profile'),
    path('students/<int:id>/achievements', achievement_views.student_achievements, name='students-achievements'),
    path('faculties/<int:id>/achievements/', achievement_views.chair_achievements, name='faculties-achievements'),
    path('faculties/<int:id>/groups', department_views.faculty_groups, name='faculties-groups'),
    path('faculties/<int:id>/profile', department_views.faculty_profile, name='faculties-profile'),
    path('faculties/<int:id>/students', user_views.department_students, name='faculties-students'),
    path('groups/', department_views.groups, name='groups'),
    path('groups/<int:id>/profile', department_views.group_profile, name='groups-profile'),
    path('groups/<int:id>/students', user_views.department_students, name='groups-students'),
    path('groups/<int:id>/achievements/', achievement_views.group_achievements, name='groups-achievements')
]
