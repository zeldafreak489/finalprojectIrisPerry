from django.shortcuts import render, redirect
from .utils import rawg_search, rawg_game_detail
from django.contrib.auth.decorators import login_required
from .models import SavedGame

# View for search results from RAWG API
def search_view(request):
    q = request.GET.get("q", "")
    results = []
    if q:
        data = rawg_search(q)
        results = data.get("results", [])
    return render(request, "library/search.html", {"query": q, "results": results})

# View for details of game from RAWG API
def detail_view(request, rawg_id):
    game = rawg_game_detail(rawg_id)
    return render(request, "library/detail.html", {"game": game})

# View for saved games in user's Library, login required
@login_required
def my_library(request):
    games = SavedGame.objects.filter(user=request.user)
    return render(request, "library/my_library.html", {"games: games"})