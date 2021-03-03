from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apis.views import (
    UserCreateView,UserLoginView,UserLogoutView,ContentCreateView
)

urlpatterns=[
    path('v1/users/login/', csrf_exempt(UserLoginView.as_view()), name='apis_v1_user_login'),
    path('v1/users/logout/', UserLogoutView.as_view(), name='apis_v1_user_logout'),
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),

    path('v1/contents/create/', csrf_exempt(ContentCreateView.as_view()), name='apis_v1_content_create'),
]