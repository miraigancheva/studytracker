from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('add/', views.grade_add, name='grade_add'),
    path('<int:pk>/', views.grade_detail, name='grade_detail'),
    path('<int:pk>/edit/', views.grade_edit, name='grade_edit'),
    path('<int:pk>/delete/', views.grade_delete, name='grade_delete'),
]
