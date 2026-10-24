from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from faculty import views

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        views.login_view,
        name="login"
    ),

    path(
        "admin-register/",
        views.admin_register,
        name="admin_register"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "manage-faculty/",
        views.manage_faculty,
        name="manage_faculty"
    ),

    path(
        "add-faculty/",
        views.add_faculty,
        name="add_faculty"
    ),

    path(
        "update-faculty/<str:faculty_id>/",
        views.update_faculty,
        name="update_faculty"
    ),

    path(
        "delete-faculty/<str:faculty_id>/",
        views.delete_faculty,
        name="delete_faculty"
    ),

    path(
        "view-faculty/<str:faculty_id>/",
        views.view_faculty,
        name="view_faculty"
    ),

    path(
        "attendance/",
        views.attendance,
        name="attendance"
    ),

    path(
        "view-attendance/",
        views.view_attendance,
        name="view_attendance"
    ),

    path(
        "delete-attendance/<str:attendance_id>/",
        views.delete_attendance,
        name="delete_attendance"
    ),

    path(
        "salary/",
        views.salary,
        name="salary"
    ),

    path(
        "add-salary/",
        views.add_salary,
        name="add_salary"
    ),

    path(
        "get-total-hours/",
        views.get_total_hours,
        name="get_total_hours"
    ),

    path(
        "view-salary/",
        views.view_salary,
        name="view_salary"
    ),

    path(
        "update-salary/<int:salary_id>/",
        views.update_salary,
        name="update_salary"
    ),

    path(
        "delete-salary/<int:salary_id>/",
        views.delete_salary,
        name="delete_salary"
    ),

    path(
        "schedule/",
        views.schedule,
        name="schedule"
    ),

    path(
        "delete-schedule/<int:schedule_id>/",
        views.delete_schedule,
        name="delete_schedule"
    ),

    path(
        "faculty-login/",
        views.faculty_login,
        name="faculty_login"
    ),

    path(
        "faculty-dashboard/",
        views.faculty_dashboard,
        name="faculty_dashboard"
    ),

    path(
        "faculty-profile/",
        views.faculty_profile,
        name="faculty_profile"
    ),

    path(
        "faculty-schedule/",
        views.faculty_schedule,
        name="faculty_schedule"
    ),

    path(
        "faculty-attendance/",
        views.faculty_attendance,
        name="faculty_attendance"
    ),
    path(
    "faculty-salary/",
    views.faculty_salary,
    name="faculty_salary"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)