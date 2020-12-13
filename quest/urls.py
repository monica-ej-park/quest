from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_xpsheets, name='xpsheets'),
    path('xpsheets/', views.show_xpsheets, name='xpsheets'),
    path('record/<str:username>/', views.record, name='record'),
    path('record/<str:username>/<str:term>/', views.record, name='record'),
    path('quests/', views.quests, name='quests'),
    path('quests/<int:data_id>/', views.quests_accomplish, name='quests_accomplish'),
    path("check/", views.check, name='check'),

]