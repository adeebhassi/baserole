# accounts/urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path("doctor/", doctor_dashboard, name="doctor_dashboard"),
    path("nurse/", nurse_dashboard, name="nurse_dashboard"),
    path("patient/", patient_dashboard, name="patient_dashboard"),
    path("pharmacist/", pharmacist_dashboard, name="pharmacist_dashboard"),
    path("select_role/", role_selection_view, name="role_selection"),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('welcome/', welcome_view, name='welcome'),
    
]
