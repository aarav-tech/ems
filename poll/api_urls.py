from django.urls import path
from poll.views import *

urlpatterns = [
    # path('poll/', poll),
    # path('poll/<int:id>/', poll_details)
    path('poll/', PollView.as_view()),
    path('poll/<int:id>/', PollDetailsView.as_view())
]