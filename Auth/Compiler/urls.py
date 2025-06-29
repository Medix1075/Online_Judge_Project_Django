from django.urls import path
from Compiler.views import submit

urlpatterns = [
    path("", submit, name="submit"),
]