from django.urls import path, include
from employee.views import *


urlpatterns = [
    path('employee/', EmployeeListView.as_view())
]