from django.urls import path, include
from poll.views import *

from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register('poll', PollViewSet)


poll_list_view = PollViewSet.as_view({
    "get": "list",
    "post": "create"
})

urlpatterns = [
    path('', include(router.urls)),
    # path('poll/', PollAPIView.as_view()),
    # path('poll/<int:id>/', PollDetailView.as_view()),
    # path('generics/poll/', poll_list_view),
    # path('generics/poll/<int:id>/', PollListView.as_view()),
    # path('poll/search/', QuestionSearchViewSet.as_view({'get': 'list'})),
]