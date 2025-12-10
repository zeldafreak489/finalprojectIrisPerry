from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Follow
from django.shortcuts import get_object_or_404
from library.models import SavedGame, Review
from activity.models import Activity

# view for signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:signup")

        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect("home")
        except:
            messages.error(request, "Username already taken.")
            return redirect("accounts:signup")

    return render(request, "accounts/signup.html")

# view for login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")

# view for logout
def logout_view(request):
    logout(request)
    return redirect("home")

# View for Account Settings
@login_required
def account_settings(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        pwd_form = PasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect('accounts:profile')
        elif 'change_password' in request.POST:
            if pwd_form.is_valid():
                user = pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been changed!")
                return redirect('accounts:profile')
            
    else: 
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        pwd_form = PasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pwd_form': pwd_form,
    }

    return render(request, 'accounts/settings.html', context)

# View for User Profile
from activity.models import Activity

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    # Existing counts
    rating_count = Review.objects.filter(user=profile_user).exclude(rating=None).count()
    review_count = Review.objects.filter(user=profile_user).count()
    playing_count = SavedGame.objects.filter(user=profile_user, shelf="playing").count()
    completed_count = SavedGame.objects.filter(user=profile_user, shelf="played").count()

    follower_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    # Real activity feed
    activities = Activity.objects.filter(user=profile_user).order_by("-created_at")[:20]

    context = {
        "profile_user": profile_user,
        "follower_count": follower_count,
        "following_count": following_count,
        "rating_count": rating_count,
        "review_count": review_count,
        "playing_count": playing_count,
        "completed_count": completed_count,
        "activities": activities,
    }

    return render(request, "accounts/user_profile.html", context)


# View for Follow/Unfollow
@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target
    )

    if not created:
        follow.delete()
        action = "unfollowed"
    else:
        action = "followed"

    # If request is AJAX
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "status": action,
            "follower_count": Follow.objects.filter(following=target).count(),
        })

    # Otherwise normal redirect
    return redirect("accounts:user_profile", username=target.username)

# View to allow users to search for one another
@login_required
def user_search(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = User.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

    context = {
        "query": query,
        "results": results
    }

    return render(request, "accounts/user_search.html", context)