from django.contrib import admin
from django.urls import path
import app.views
from app.services.auth_service import AuthService
from app.services.account_service import AccountService
from app.services.course_service import CourseService
from app.services.ta_service import TaService

deps = {
    'auth_service': AuthService(),
    'account_service': AccountService(),
    'course_service': CourseService(),
    'ta_service': TaService()
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", app.views.Dashboard.as_view(**deps)),
    path("dashboard/", app.views.Dashboard.as_view(**deps)),
    path("view_contact_info/", app.views.ViewAccounts.as_view(**deps)),
    path("login/", app.views.Login.as_view(**deps)),
    path("logout/", app.views.Logout.as_view(**deps)),
    path("cr_account/", app.views.CreateAccount.as_view(**deps)),
    path("edit_account/", app.views.EditAccount.as_view(**deps)),
    path("update_contact/", app.views.UpdateContactInfo.as_view(**deps)),
    path("view_courses/", app.views.ViewCourses.as_view(**deps)),
    path("my_courses/", app.views.MyCourses.as_view(**deps)),
    path("course_details/", app.views.CourseDetails.as_view(**deps)),
    path("assign_ta_course/", app.views.AssignTaCourse.as_view(**deps)),
    path("cr_lab/", app.views.CreateLab.as_view(**deps)),
    path("cr_course/", app.views.CreateCourse.as_view(**deps)),
    path("set_password/", app.views.SetPassword.as_view()),
    path("assign_ins/", app.views.AssignInstructor.as_view(**deps)),
    path("assign_ta_labs/", app.views.AssignTaLabs.as_view(**deps)),
    path("my_courses_ta/", app.views.MyCoursesTa.as_view(**deps))
]
