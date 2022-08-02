from django.urls import path
from .import views

urlpatterns = [     
    path('', views.IndexView.as_view(), name='index'),
    path('page/<str:slug>/', views.IndexView.as_view(), name='index_id'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login-user/', views.login_view, name='login-user'),
    path('logout-user/', views.logout_view, name='logout-user'),

    path('search/', views.search, name='query_slug'),
    path('search/<int:pk>', views.search, name='query_id'),
]