from itertools import chain

from accounts.models import User
from core.forms import FollowsForm, ReviewForm, TicketForm
from core.models import Review, Ticket, UserBlock, UserFollows
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import CharField, Q, Value
from django.shortcuts import get_object_or_404, redirect, render
from el_pagination.decorators import page_template
from django.http import JsonResponse


@login_required
@page_template("core/partials/posts_feed.html")
def feed(request, template="core/feed.html", extra_context=None):

    tickets = get_feed_tickets(request.user).filter(part_of_full_review=False)
    reviews = get_feed_reviews(request.user)
    posts = get_posts_feed(tickets, reviews)

    context = {"posts": posts}
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def get_feed_tickets(user):
    """
    Retrieves tickets visible in user's feed: own and from followed users.
    """
    return Ticket.objects.filter(
        Q(user=user) | Q(user__in=user.following.values("followed_user"))
    )


def get_feed_reviews(user):
    """
    Retrieves reviews visible in feed: own, from followed users, or about own tickets.
    """
    return Review.objects.filter(
        Q(user=user)
        | Q(user__in=user.following.values("followed_user"))
        | Q(ticket__user=user)
    )


@login_required
@page_template("core/partials/personal_posts_feed.html")
def personal_posts(request, template="core/personal_posts.html", extra_context=None):
    """
    Personal posts view showing only the authenticated user's content.
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    posts = get_posts_feed(tickets, reviews)

    context = {"posts": posts}
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def get_posts_feed(tickets, reviews):
    """
    Merges tickets and reviews into unified feed with type annotations.

    Annotates each queryset with content_type ('TICKET'/'REVIEW') and combines them
    chronologically (newest first) using time_created.
    """
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    return sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )


def check_object_owner(model_object, id, owner="user"):
    """Factory creating decorators verifying object ownership before view execution."""

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            object = get_object_or_404(model_object, id=kwargs[id])
            if getattr(object, owner) != request.user:
                raise PermissionDenied
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


@login_required
def create_ticket(request):
    """
    Handles ticket creation with file upload capability.
    """
    ticket_form = TicketForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("feed")
    return render(
        request, "core/create_ticket.html", context={"ticket_form": ticket_form}
    )


@login_required
@check_object_owner(Ticket, "ticket_id")
def change_ticket(request, ticket_id):
    """Edits existing ticket with ownership verification."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket.save()
            return redirect("posts")
    else:
        ticket_form = TicketForm(instance=ticket)
    return render(request, "core/change_ticket.html", {"ticket_form": ticket_form})


@login_required
@check_object_owner(Ticket, "ticket_id")
def delete_ticket(request, ticket_id):
    """Confirms and deletes user-owned ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect("posts")
    return render(request, "core/delete_ticket.html", {"ticket": ticket})


@login_required
def create_review(request, ticket_id):
    """Handles review creation and prevents duplicate reviews on tickets"""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.user == request.user:
        raise PermissionDenied
    if Review.objects.filter(ticket=ticket).exists():
        if (
            ticket.part_of_full_review
            and Review.objects.filter(ticket=ticket).count() >= 2
        ):
            raise PermissionDenied
        elif not ticket.part_of_full_review:
            raise PermissionDenied

    review_form = ReviewForm()
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
    return render(
        request,
        "core/create_review.html",
        context={"review_form": review_form, "ticket": ticket},
    )


@login_required
@check_object_owner(Review, "review_id")
def change_review(request, ticket_id, review_id):
    """Edits existing review with ownership verification."""
    review = get_object_or_404(Review, id=review_id, ticket_id=ticket_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review.save()
            return redirect("posts")
    else:
        review_form = ReviewForm(instance=review)
    return render(
        request, "core/change_review.html", context={"review_form": review_form}
    )


@login_required
@check_object_owner(Review, "review_id")
def delete_review(request, ticket_id, review_id):
    """Confirms and deletes user-owned review."""
    review = get_object_or_404(Review, id=review_id, ticket_id=ticket_id)
    if request.method == "POST":
        review.delete()
        return redirect("posts")
    return render(request, "core/delete_review.html", context={"review": review})


@login_required
def create_full_review(request):
    """Handles user's full review creation."""
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.part_of_full_review = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
    return render(
        request,
        "core/create_full_review.html",
        context={"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def follow_user(request):
    """
    Handles user follow/unfollow flows with search functionality.

    Manages:
    - User search (5 max results)
    - Follow validation (clean checks)
    - Context with relations/blocked users
    """
    follows_form = FollowsForm()
    blocked_users = UserBlock.objects.filter(blocker=request.user)
    context = {
        "follows_form": follows_form,
        "following": request.user.following.all(),
        "followers": request.user.followed_by.all(),
        "search_results": User.objects.none(),
        "blocked_users": blocked_users,
    }

    if request.method == "POST":

        if "search" in request.POST:
            username = request.POST.get("username")
            search_results = User.objects.filter(username__icontains=username).exclude(
                username=request.user
            )[:5]
            context["search_results"] = search_results
            if not search_results.exists():
                messages.info(request, "La recherche n'a donné aucun résultat.")

        if "follow" in request.POST:
            follows_form = FollowsForm(request.POST)
            if follows_form.is_valid():
                try:
                    user_to_follow = User.objects.get(
                        username=follows_form.cleaned_data["username"]
                    )
                    follow = UserFollows(
                        user=request.user, followed_user=user_to_follow
                    )
                    follow.full_clean()
                    follow.save()
                    messages.success(
                        request, f"Vous suivez maintenant {follow.followed_user}."
                    )
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                except User.DoesNotExist:
                    messages.error(
                        request,
                        f"L'utilisateur {follows_form.cleaned_data['username']}"
                        "n'existe pas.",
                    )

    return render(request, "core/follow.html", context=context)


@login_required
def unfollow_user(request, follows_id):
    """Unfollows user and redirects."""
    UserFollows.objects.get(id=follows_id, user=request.user).delete()
    return redirect("follow")


@login_required
def block_user(request, user_id):
    """Blocks follower and removes follow relation."""
    follow = get_object_or_404(UserFollows, id=user_id, followed_user=request.user)
    blocked_user = UserBlock.objects.create(blocker=request.user, blocked=follow.user)
    follow.delete()
    messages.success(request, f"Vous avez bloqué {blocked_user.blocked.username}")
    return redirect("follow")


@login_required
def unblock_user(request, block_id):
    """Removes block and redirects."""
    block = get_object_or_404(UserBlock, id=block_id, blocker=request.user)
    block.delete()
    return redirect("follow")


def api_user_search(request):
    if not request.GET.get("q"):
        return JsonResponse({"error": "Paramètre 'q' manquant"}, status=400)

    users = User.objects.filter(username__icontains=request.GET["q"]).exclude(
        username=request.user.username
    )[:3]

    return JsonResponse(
        {"results": [{"username": user.username, "id": user.id} for user in users]}
    )
