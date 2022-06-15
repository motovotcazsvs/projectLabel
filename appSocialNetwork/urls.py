from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signup/', views.signup_page, name = 'signup'),
    path('login/', views.login_page, name = "login"),  
	path('logout/', views.logout_page, name = "logout"),
    path('mylabel/', views.myLabel, name = "mylabel"),
    path('mylabel/addpublication/', views.addPublication, name = "addpublication"),
    path('<int:pagePost_id>/', views.pagePost, name = 'pagePost'),
    path('like/', views.like_post, name = 'like_post'),    
]

