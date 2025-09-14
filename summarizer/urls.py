# route to the summarizer view.

from django.urls import path
from . import views

urlpatterns = [
    path("", views.summarizer_view, name="summarizer_view"),
]
