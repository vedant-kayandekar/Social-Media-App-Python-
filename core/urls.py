from django.urls import path  
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('follow2', views.follow2, name='follow2'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('profile2/<str:pk>', views.profile2, name='profile2'),
    path('like-post', views.like_post, name='like-post'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    # path('<int:pk>/add-comment',views.add_comment, name='add-comment')
    # path('login/',views.login, name="login"),
    ]


