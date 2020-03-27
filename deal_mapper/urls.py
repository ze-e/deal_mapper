from django.urls import path
from django.conf import settings
from . import views

urlpatterns=[
    path('',views.index, name='index'),
    path('api/properties/', views.Current_Property_List_Create.as_view() ),
] 