from django.urls import path
from . import views


urlpatterns = [
    path('reject', views.reject, name="reject"),
    path('accept', views.accept, name="accept"),
    path('approve', views.approve, name="approve"),
    path('not_approve', views.not_approve, name="not_approve"),
]

