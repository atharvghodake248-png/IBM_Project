from django.urls import path

from . import api_views, views

urlpatterns = [
    path("", views.home, name="home"),
    path("dealers/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("dealers/<int:dealer_id>/review/", views.post_review, name="post_review"),
    path("accounts/login/", views.sign_in, name="login"),
    path("accounts/register/", views.register, name="register"),
    path("djangoapp/login", api_views.django_login, name="django_login"),
    path("djangoapp/logout", api_views.django_logout, name="django_logout"),
    path("fetchDealers", api_views.fetch_dealers, name="fetch_dealers"),
    path("fetchDealer/<int:dealer_id>", api_views.fetch_dealer, name="fetch_dealer"),
    path("fetchDealers/<str:state>", api_views.fetch_dealers_by_state, name="fetch_dealers_by_state"),
    path("fetchReviews/dealer/<int:dealer_id>", api_views.fetch_reviews, name="fetch_reviews"),
    path("analyze/<str:review_text>", api_views.analyze_review, name="analyze_review"),
    path("getallcarmakes", api_views.fetch_car_makes, name="fetch_car_makes"),
]
