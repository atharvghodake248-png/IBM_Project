from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dealers/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("dealers/<int:dealer_id>/review/", views.post_review, name="post_review"),
    path("accounts/login/", views.sign_in, name="login"),
    path("accounts/register/", views.register, name="register"),
]
