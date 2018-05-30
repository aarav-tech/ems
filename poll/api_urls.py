from django.urls import path
from poll.views import *

urlpatterns = [
    # path('poll/', poll),
    path('poll/', PollAPIView.as_view()),
    path('poll/<int:id>/', PollDetailView.as_view()),
    path('generics/poll/', PollListView.as_view()),
    path('generics/poll/<int:id>/', PollListView.as_view())
]