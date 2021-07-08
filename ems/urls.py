"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

from django.conf import settings


from employee.views import ( index, user_login, user_logout,
    success, ProfileUpdate, MyProfile, LoginView, LogoutView)

schema_view = get_swagger_view(title='EMS API Documentation')

urlpatterns = [
    path('api_documentation/', schema_view),
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('poll/', include('poll.urls')),
    path('api/v1/', include('poll.api_urls')),
    path('api/v1/', include('employee.api_urls')),
    # path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/login/', LoginView.as_view()),
    path('api/v1/auth/logout/', LogoutView.as_view()),
    path('employee/', include('employee.urls')),

    path('login/', user_login, name="user_login"),
    path('success/', success, name="user_success"),
    path('logout/', user_logout, name="user_logout"),
    path('profile/', MyProfile.as_view(), name="my_profile"),
    path('profile/update', ProfileUpdate.as_view(), name="update_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
