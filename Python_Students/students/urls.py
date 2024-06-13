from django.urls import path
from . import views
from .views import (
    add_subject,
    add_schedule,
    add_batch_subject,
    add_course,
    edit_grade,
)

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('student/add/', views.student_add, name='student_add'),
    path('group/add/', views.group_add, name='group_add'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/add_subject/', add_subject, name='add_subject'),
    path('subjects/<int:pk>/add_schedule/', add_schedule, name='add_schedule'),
    path('add_batch_subject/', add_batch_subject, name='add_batch_subject'),
    path('add_course/', add_course, name='add_course'),
    path('students/course/<int:pk>/edit_grade/', edit_grade, name='edit_grade'),
    path('students/student_course/<int:pk>/delete/', views.delete_student_course, name='delete_student_course'),
    path('students/<int:student_id>/add_existing_course/', views.add_existing_course, name='add_existing_course'),
    path('manage_subjects/', views.manage_subjects, name='manage_subjects'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('students/<int:pk>/edit_student_course/', views.edit_student_course, name='edit_student_course'),
    path('toggle_student_debt/<int:pk>/', views.toggle_student_debt, name='toggle_student_debt'),
    path('debts/', views.student_debt_list, name='student_debt_list'),
]
