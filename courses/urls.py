from django.urls import path
from courses.views import *

app_name = 'courses'

urlpatterns = [
    path('create/', create_course_view, name='create_course'),
    path('my_courses/', my_courses_view, name='my_courses'),
    path('<int:course_id>/add-module/', add_module_view, name='add_module'),
    path('module/<int:module_id>/add-lesson/', add_lesson_view, name='add_lesson'),
    path('<int:course_id>/', course_detail_view, name='course_detail'),
    path('module/<int:module_id>/edit/', edit_module_view, name='edit_module'),
    path('lesson/<int:lesson_id>/edit/', edit_lesson_view, name='edit_lesson'),
    path('module/<int:module_id>/delete/', delete_module_view, name='delete_module'),
    path('lesson/<int:lesson_id>/delete/', delete_lesson_view, name='delete_lesson'),
    path('<int:course_id>/enroll/', enroll_in_course, name='enroll_course'),
    path('browse/', browse_courses_view, name='browse_courses'),
    path('my-learning/', my_learning_view, name='my_learning'),
    path('lesson/<int:lesson_id>/', lesson_detail_view, name='lesson_detail'),
    path('lesson/<int:lesson_id>/complete/', mark_lesson_complete, name='mark_lesson_complete'),
    path('course/<int:course_id>/certificate/', download_certificate, name='download_certificate'),
    path('<int:course_id>/edit/', edit_course_view, name='edit_course'),
    path('<int:course_id>/checkout/', checkout_view, name='checkout'),
    path('<int:course_id>/verify/', verify_payment_view, name='verify_payment'),
    path('course/<int:course_id>/quiz/create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-question/', add_question, name='add_question'),
    path('quiz/<int:quiz_id>/attempt/', attempt_quiz_view, name='attempt_quiz'),
    path('quiz/<int:attempt_id>/result/', view_result_view, name='view_result'),
    path('course/<int:course_id>/quizzes/', instructor_quizzes_view, name='instructor_quizzes'),
    path('quiz/<int:quiz_id>/attempts/', quiz_attempts_list_view, name='quiz_attempts_list'),


]
