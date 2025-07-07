from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('list/', views.problem_list, name='problem_list'),
    path('problems/<int:pk>/', views.problem_detail, name='problem_details'),
    path('problems/create/', views.problem_create, name='problem_form'),
    path('problem/<int:pk>/generate-review/', views.generate_ai_review, name='generate_ai_review'),
]