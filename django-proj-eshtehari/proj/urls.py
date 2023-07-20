from django.urls import path, include
from .views import *
from rest_framework import routers # API
from rest_framework.authtoken import views # API

# API
router = routers.DefaultRouter()
router.register('news', NewsViewSet)
router.register('lists', UniqueListView, basename='news-lists')

# print(router.urls)

urlpatterns = [
    path("", redir_view),
    path('api/', include(router.urls)), # API
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')), # API
    # path('api/lists/', UniqueListView.as_view(), name='lists'),
]
