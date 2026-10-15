import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Dealer, Review


def dealer_data(dealer):
    return {
        "id": dealer.id,
        "city": dealer.city,
        "state": dealer.state,
        "full_name": dealer.name,
        "short_name": dealer.short_name or dealer.name,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.lat,
        "long": dealer.long,
    }


@require_GET
def fetch_dealers(request):
    return JsonResponse({
        "dealers": [dealer_data(d) for d in Dealer.objects.all()]
    })


@require_GET
def fetch_dealer(request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    return JsonResponse(dealer_data(dealer))


@require_GET
def fetch_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state)
    return JsonResponse({
        "dealers": [dealer_data(d) for d in dealers]
    })


@require_GET
def fetch_reviews(request, dealer_id):
    reviews = Review.objects.filter(
        dealer_id=dealer_id
    ).select_related("user", "dealer")
    data = [
        {
            "id": r.id,
            "name": r.user.get_full_name() or r.user.username,
            "reviewer": r.user.get_full_name() or r.user.username,
            "review": r.text,
            "rating": r.rating,
            "purchase": r.purchase,
            "car_make": r.car_make,
            "car_model": r.car_model,
            "car_year": r.car_year,
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ]
    return JsonResponse({"reviews": data})


@require_GET
def analyze_review(request, review_text=""):
    text = (review_text or request.GET.get("review", "")).strip().lower()
    positive = (
        "fantastic", "excellent", "great", "good",
        "amazing", "wonderful", "helpful",
    )
    negative = (
        "bad", "poor", "terrible", "awful", "worst", "horrible",
    )
    if any(word in text for word in positive):
        sentiment = "positive"
    elif any(word in text for word in negative):
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return JsonResponse({"sentiment": sentiment})


@require_GET
def fetch_car_makes(request):
    return JsonResponse({"CarMakes": [
        {"id": 1, "name": "Toyota", "models": ["Camry", "Corolla"]},
        {"id": 2, "name": "Honda", "models": ["Civic", "Accord"]},
        {"id": 3, "name": "Ford", "models": ["Focus", "Mustang"]},
    ]})


@csrf_exempt
@require_POST
def django_login(request):
    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"userName": "", "status": "Invalid JSON"}, status=400)

    username = data.get("userName") or data.get("username") or ""
    password = data.get("password") or ""
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse(
            {"userName": "", "status": "Invalid credentials"}, status=401
        )

    login(request, user)
    return JsonResponse({
        "userName": user.username,
        "status": "Authenticated",
    })
@require_GET
def django_logout(request):
    logout(request)
    return JsonResponse({"userName": ""})

