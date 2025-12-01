from django.shortcuts import render, redirect
from .utils import rawg_search, rawg_game_detail
from django.contrib.auth.decorators import login_required
from .models import SavedGame
from django.contrib import messages
from types import SimpleNamespace

# View for search results from RAWG API
def search_view(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # Convert dicts to objects
        results = [SimpleNamespace(**g) for g in rawg_search(query) if g.get("id")]

    # Get IDs of user's saved games to prevent adding duplicates to user's library.
    if request.user.is_authenticated:
        user_saved_ids = set(SavedGame.objects.filter(user=request.user).values_list('rawg_id', flat=True))
    else:
        user_saved_ids = set()
        
    return render(request, "library/search.html", {
        "results": results, 
        "query": query,
        "user_saved_ids": user_saved_ids
    })

# View for details of game from RAWG API
def detail_view(request, rawg_id):
    game = rawg_game_detail(rawg_id)

    # Check if the game is already in the user's library
    saved_game = None
    if request.user.is_authenticated:
        try:
            saved_game = SavedGame.objects.get(user=request.user, rawg_id=rawg_id)
        except SavedGame.DoesNotExist:
            saved_game = None

    return render(
        request, 
        "library/detail.html", 
        {"game": game, "saved_game": saved_game}, 
    )

# View for saved games in user's Library, login required
@login_required
def my_library(request):
    games = SavedGame.objects.filter(user=request.user)
    return render(request, "library/my_library.html", {"games": games})

# View for adding game to library, login required
@login_required
def add_to_library(request, rawg_id):
    if request.method == "POST":
        title = request.POST.get("title")
        cover = request.POST.get("cover")
        status = request.POST.get("status", "want")

        # Prevent duplicate saved games
        saved_game, created = SavedGame.objects.get_or_create(
            user=request.user,
            rawg_id=rawg_id,
            defaults={"title": title, "cover_image": cover, "status": status},
        )
        if not created:
            # If the game already exists, update the status
            saved_game.status = status
            saved_game.save()
            messages.success(request, f"{title} status updated in your library!")
        else:
            messages.success(request, f"{title} added to your library!")

    # redirect back to game detail page
    game = rawg_game_detail(rawg_id)
    try:
        saved_game = SavedGame.objects.get(user=request.user, rawg_id=rawg_id)
    except SavedGame.DoesNotExist:
        saved_game = None

    return render(request, "library/detail.html", {"game": game, "saved_game": saved_game})