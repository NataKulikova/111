
from django.urls import path
from .views import PostView, PostDetail, PostCreate, PostEdit, ResponseCreate, ResponseList, ResponseDelete, ResponseAccept, subscriptions
from allauth.account.views import LogoutView, LoginView, SignupView

urlpatterns = [

    path('', PostView.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('edit/<int:pk>', PostEdit.as_view(), name='post_edit'),
    path('accounts/logout', LogoutView.as_view(), name='account_logout'),
    path('accounts/login', LoginView.as_view(), name='account_login'),
    path('accounts/signup', SignupView.as_view(), name='account_signup'),
    path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
    path('responses', ResponseList.as_view(), name='responses'),
    path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('responses/<int:pk>/accept', ResponseAccept.as_view(), name='response_accept'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
