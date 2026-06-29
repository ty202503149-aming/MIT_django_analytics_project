from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_home, name='analytics_home'),
    path('train/', views.train_model, name='train_model'),
    path('predict/', views.predict, name='predict'),
]