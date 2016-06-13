from django.shortcuts import render, redirect
from .models import UserModel

# Create your views here.


def profile(request):

    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    return render(request, "user_profile/profile_page.html", {})
