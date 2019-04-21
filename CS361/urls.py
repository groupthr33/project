from django.contrib import admin
from django.urls import path
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", app.views.Dashboard.as_view()),
    path("dashboard/", app.views.Dashboard.as_view()),
    path("view_contact_info/", app.views.ViewAccounts.as_view()),
    path("login/", app.views.Login.as_view()),
    path("logout/", app.views.Logout.as_view()),
    path("cr_account/", app.views.CreateAccount.as_view()),
    path("edit_account/", app.views.EditAccount.as_view()),
    path("update_contact/", app.views.UpdateContactInfo.as_view()),
    path("view_courses/", app.views.ViewCourses.as_view()),
    path("my_courses/", app.views.MyCourses.as_view()),
    path("course_details/", app.views.CourseDetails.as_view()),
    path("assign_ta_course/", app.views.AssignTaCourse.as_view()),
    path("assign_ins/", app.views.AssignInstructor.as_view()),
]