from django.shortcuts import get_object_or_404, render, redirect
from .utils import rawg_search, rawg_game_detail
from django.contrib.auth.decorators import login_required
from .models import SavedGame
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Review
from .forms import ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from types import SimpleNamespace
from activity.models import Activity

# View for search results from RAWG API
def search_view(request):
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    results = []

    if query:
        # Check the cache first
        cache_key = f"search_{query.lower()}"
        cached_results = cache.get(cache_key)
        if cached_results:
            data = cached_results
        else:
            # fetch from RAWG API
            data = rawg_search(query)
            cache.set(cache_key, data, 60*15) # cache for 15 mins

        # convert dicts to objects for template access
        results = [SimpleNamespace(**g) for g in data if g.get("id")]

    # Paginate the results (12 per page)
    paginator = Paginator(results, 12)
    try:
        paginated_results = paginator.page(page)
    except PageNotAnInteger:
        paginated_results = paginator.page(1)
    except EmptyPage:
        paginated_results = paginator.page(paginator.num_pages)

    # Get user's saved game IDs
    if request.user.is_authenticated:
        user_saved_ids = set(
            SavedGame.objects.filter(user=request.user).values_list("rawg_id", flat=True)
        )
    else:
        user_saved_ids = set()

    return render(request, "library/search.html", {
        "results": paginated_results,
        "query": query,
        "user_saved_ids": user_saved_ids,
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

    reviews = Review.objects.filter(rawg_id=rawg_id).order_by("-created_at")

    # Extra info including description, genres, esrb rating, franchises, and system requirements
    extra_info = {
        "description": game.get("description_raw", ""),
        "genres": [g["name"] for g in game.get("genres", [])],
        "esrb": game.get("esrb_rating", {}).get("name", "N/A"),
        "franchises": [f["name"] for f in game.get("franchises", [])],
    }

    context = {
        "game": game,
        "saved_game": saved_game,
        "reviews": reviews,
        "extra_info": extra_info,
    }

    return render(request, "library/detail.html", context)

# View for saved games in user's Library, login required
@login_required
def my_library(request):
    shelf = request.GET.get("shelf")
    games = SavedGame.objects.filter(user=request.user)

    if shelf in ["want", "playing", "played"]:
        games = games.filter(shelf=shelf)
    return render(request, "library/my_library.html", {"games": games, "active_shelf": shelf})

# View for adding game to library, login required
@login_required
@require_POST
def add_to_library(request, rawg_id):
    title = request.POST.get("title")
    cover = request.POST.get("cover")
    shelf = request.POST.get("status", "want")

    saved_game, created = SavedGame.objects.get_or_create(
        user=request.user,
        rawg_id=rawg_id,
        defaults={"title": title, "cover_image": cover, "shelf": shelf},
    )

    if not created:
        saved_game.shelf = shelf
        saved_game.save()
        message = f"{title} shelf updated!"
    else:
        message = f"{title} added to your library!"

    Activity.objects.create(
        user=request.user,
        game_title=title,
        activity_type="add" if created else "status",
    )

    return JsonResponse({
        "success": True,
        "message": message,
        "rawg_id": rawg_id,
        "shelf": saved_game.get_shelf_display(),
    })

# View for rating and reviewing games
@login_required
def add_review(request, rawg_id):
    try:
        review = Review.objects.get(user=request.user, rawg_id=rawg_id)
    except Review.DoesNotExist:
        review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.rawg_id = rawg_id
            new_review.save()
            messages.success(request, "Your review has been saved!")
            return redirect('library:detail', rawg_id=rawg_id)
    else:
        form = ReviewForm(instance=review)

    # Pass the star range to the template
    stars = [x / 4 for x in range(0, 21)]

    return render(request, 'library/add_review.html', {'form': form, 'rawg_id': rawg_id, 'stars': stars})

# View for updating shelf from my_library.html
@login_required
@require_POST
def update_shelf(request, rawg_id):
    shelf = request.POST.get("status")
    try:
        saved_game = SavedGame.objects.get(user=request.user, rawg_id=rawg_id)
        saved_game.shelf = shelf
        saved_game.save()
        return JsonResponse({"success": True, "shelf": saved_game.shelf})
    except SavedGame.DoesNotExist:
        return JsonResponse({"success": False, "error": "Game not in library."}, status=404)
    
# Remove game from library
@login_required
@require_POST
def remove_from_library(request, rawg_id):
    game = get_object_or_404(
        SavedGame,
        user=request.user,
        rawg_id=rawg_id
    )

    game.delete()

    return JsonResponse({
        "success": True,
        "rawg_id": rawg_id,
    })
