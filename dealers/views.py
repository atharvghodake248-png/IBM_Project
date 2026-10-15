from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from .models import Dealer, Review

def home(request):
    if not Dealer.objects.exists():
        Dealer.objects.bulk_create([
            Dealer(name="Tech City", city="Wichita", state="Kansas"),
            Dealer(name="Ez PC", city="Topeka", state="Kansas"),
            Dealer(name="GH Computers", city="Austin", state="Texas"),
        ])
    state = request.GET.get("state", "")
    dealers = Dealer.objects.all()
    if state:
        dealers = dealers.filter(state__iexact=state)
    return render(request, "dealers/home.html", {"dealers": dealers, "state": state})

def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return render(request, "dealers/detail.html", {"dealer": dealer})

@login_required
def post_review(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        rating = int(request.POST.get("rating", "5"))
        if text and 1 <= rating <= 5:
            Review.objects.create(dealer=dealer, user=request.user, text=text, rating=rating)
            return redirect("dealer_detail", dealer_id=dealer.id)
    return render(request, "dealers/post_review.html", {"dealer": dealer})

def sign_in(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "dealers/login.html", {"form": form})
