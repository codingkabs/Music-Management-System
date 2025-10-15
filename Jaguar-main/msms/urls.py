"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

from lessons import old_views
from lessons.views import administrator, shared, student, director

main_patterns = [
    path("", old_views.home, name="home"),
    path("login/", old_views.log_in, name="log_in"),
    path("logout/", old_views.log_out, name="log_out"),
    path("signup/", old_views.sign_up, name="sign_up"),
    path("admin/", admin.site.urls),
    path("student/", old_views.student, name="student"),
    path("administrator/", old_views.administrator, name="administrator"),
    path("director/", old_views.director, name="director"),
]

student_lesson_requests_patterns = [
    path("", student.lesson_requests, name="student/lesson-requests"),
    path("view/<int:lesson_request_id>", shared.view_lesson_request, name="student/lesson-requests/view"),
    path("edit/<pk>", shared.LessonRequestUpdateView.as_view(), name="student/lesson-requests/edit"),
    path("delete/<pk>", shared.LessonRequestDeleteView.as_view(), name="student/lesson-requests/delete"),
    path("view-lessons/<int:lesson_request_id>", student.view_lessons, name="student/lesson-requests/view-lessons"),
]

student_patterns = [
    path("lesson_request/", student.lesson_request, name="student/lesson-request"),
    path("booked-lessons", student.booked_lessons, name="student/booked-lessons"),
    path("lesson-requests/", include(student_lesson_requests_patterns)),
    path("invoices/", student.invoices, name="student/invoices"),
]

administrator_patterns = [
    path("lesson-requests", administrator.lesson_requests, name="administrator/lesson-requests"),
    path("lesson-requests/view/<int:lesson_request_id>",
         shared.view_lesson_request,
         name="administrator/lesson-requests/view"),
    path("lesson-requests/book/<int:lesson_request_id>",
         old_views.administrator_lesson_requests_book,
         name="administrator/lesson-requests/book"),
    path("lesson-requests/book/<int:lesson_request_id>/finalise-booking",
         old_views.administrator_lesson_requests_book_finalise_booking,
         name="administrator/lesson-requests/book/finalise-booking"),
    path("delete/<pk>", shared.LessonRequestDeleteView.as_view(), name="administrator/lesson-requests/delete"),
    path("edit/<pk>", shared.LessonRequestUpdateView.as_view(), name="administrator/lesson-requests/edit"),
    path("book/<int:lesson_request_id>/lessons/delete/<pk>",
         old_views.AdministratorLessonDeleteView.as_view(),
         name="administrator/lesson-requests/book/lessons/delete"),
    path("book/<int:lesson_request_id>/lessons/edit/<pk>",
         old_views.AdministratorLessonUpdateView.as_view(),
         name="administrator/lesson-requests/book/lessons/edit"),
    path("book/<int:lesson_request_id>/lessons/create",
         old_views.AdministratorLessonCreateView.as_view(),
         name="administrator/lesson-requests/book/lessons/create"),
    path("student-balances", administrator.student_balances, name="administrator/student-balances"),
]

director_patterns = [
    path("lesson-requests", old_views.director_lesson_requests, name="director/lesson-requests"),
    path("student-balances", old_views.director_student_balances, name="director/student-balances"),
    path("manage-administrators", director.administrator_list, name="director/manage-administrators"),
    path("manage-administrators/create-administrator",
         old_views.director_create_administrator,
         name="director/manage-administrators/create-administrator"),
    path("manage-administrators/edit/<pk>",
         director.AdminUpdateView.as_view(),
         name="director/manage-administrators/edit"),
    path("manage-administrators/delete/<pk>",
         director.AdminDeleteView.as_view(),
         name="director/manage-administrators/delete"),
]

urlpatterns = [
    path("", include(main_patterns)),
    path("student/", include(student_patterns)),
    path("administrator/", include(administrator_patterns)),
    path("director/", include(director_patterns)),
]