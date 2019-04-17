from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Dashboard.as_view()),
    path("cmd/", views.Home.as_view()),
    path("dashboard/", views.Dashboard.as_view()),
    path("sample_command/", views.SampleRoute.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("cr_account/", views.CreateAccount.as_view())
]
