# 2101940 Kyle Keene-Welch
# urls.py
# Sub url file that contains all the routes a user can take to render and interact with the site.

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('following/', views.showFollowers, name="show-following"),
    path('favourites/<str:pk>', views.showFavourites, name="show-favourites"),
    path('create-room/', views.createRoom, name="create-room"),
    path('create-material/<str:pk>', views.createMaterial, name="create-material"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('update-material/<str:pk>', views.updateMaterial, name="update-material"),
    path('update-user', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activities"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('delete-material/<str:pk>', views.deleteMaterial, name="delete-material"),
    path('set-favourite/<str:pk>', views.setFavourite, name="set-favourite"),
    path('remove-favourite/<str:pk>', views.removeFavourite, name="remove-favourite"),
    path('unfollow/<str:pk>', views.unfollow, name='unfollow'),
]