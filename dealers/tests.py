from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Dealer, Review


class DealerApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            name="Test Dealer",
            city="Wichita",
            state="Kansas",
            address="123 Main Street",
            zip="67202",
            lat="37.6872",
            long="-97.3301",
        )
        self.user = User.objects.create_user(
            username="reviewer", password="test-password-123"
        )

    def test_fetch_dealers_returns_location_fields(self):
        response = self.client.get("/fetchDealers")
        self.assertEqual(response.status_code, 200)
        dealer = response.json()["dealers"][0]
        for field in ("address", "zip", "lat", "long", "short_name", "full_name"):
            self.assertIn(field, dealer)

    def test_fetch_dealer(self):
        response = self.client.get(f"/fetchDealer/{self.dealer.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["city"], "Wichita")

    def test_filter_by_state(self):
        response = self.client.get("/fetchDealers/Kansas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_reviews_include_purchase_and_car_fields(self):
        Review.objects.create(
            dealer=self.dealer,
            user=self.user,
            rating=5,
            text="Fantastic services",
            purchase="2026-01-10",
            car_make="Toyota",
            car_model="Camry",
            car_year=2024,
        )
        response = self.client.get(
            f"/fetchReviews/dealer/{self.dealer.id}"
        )
        self.assertEqual(response.status_code, 200)
        review = response.json()["reviews"][0]
        for field in ("purchase", "car_make", "car_model", "car_year"):
            self.assertIn(field, review)

    def test_sentiment_positive(self):
        response = self.client.get("/analyze/Fantastic%20services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "positive")

    def test_invalid_login_rejected(self):
        response = self.client.post(
            "/djangoapp/login",
            data='{"username":"wrong","password":"wrong"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
