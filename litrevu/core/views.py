from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q, CharField, Value
from django.shortcuts import render, redirect, get_object_or_404

from itertools import chain

from accounts.models import User
from core.forms import TicketForm, ReviewForm, FollowsForm
from core.models import Ticket, Review, UserFollows


@login_required
def feed(request):
    tickets = get_feed_tickets(request.user)
    reviews = get_feed_reviews(request.user)
    posts = get_posts_feed(tickets, reviews)
    return render(request, 'core/feed.html', context={'posts': posts})


def get_feed_tickets(user):
    return Ticket.objects.filter(
        Q(user=user) |
        Q(user__in=user.following.values('followed_user')))


def get_feed_reviews(user):
    return Review.objects.filter(
        Q(user=user) |
        Q(user__in=user.following.values('followed_user')) |
        Q(ticket__user=user))


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    posts = get_posts_feed(tickets, reviews)
    return render(request, 'core/posts.html', context={'posts': posts})


def get_posts_feed(tickets, reviews):
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    return sorted(chain(tickets, reviews), key=lambda post: post.time_created, reverse=True)


@login_required
def create_ticket(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    return render(request, 'core/create_ticket.html', context={'ticket_form': ticket_form})


@login_required
def change_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket.save()
            return redirect('posts')
    else:
        ticket_form = TicketForm(instance=ticket)
    return render(request, 'core/change_ticket.html', {'ticket_form': ticket_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 'core/delete_ticket.html', {'ticket': ticket})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    return render(request, 'core/create_review.html', context={'review_form': review_form, 'ticket': ticket})


@login_required
def change_review(request, ticket_id, review_id):
    ticket = Review.objects.get(id=ticket_id)
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review.save()
            return redirect('posts')
    else:
        review_form = ReviewForm(instance=review)
    return render(request, 'core/change_review.html', context={'ticket': ticket, 'review_form': review_form})


@login_required
def delete_review(request, ticket_id, review_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 'core/delete_review.html', context={'ticket': ticket, 'review': review})


@login_required
def create_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    return render(request, 'core/create_ticket_review.html', context={'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def follow_user(request):
    follows_form = FollowsForm()
    context = {
        'follows_form': follows_form,
        'following': request.user.following.all(),
        'followers': request.user.followed_by.all(),
        'search_results': User.objects.none(),
    }

    if request.method == 'POST':

        if 'search' in request.POST:
            username = request.POST.get('username')
            search_results = User.objects.filter(username__icontains=username)[:5]
            context['search_results'] = search_results
            if not search_results.exists():
                messages.info(request, "La recherche n'a donné aucun résultat.")

        if 'follow' in request.POST:
            follows_form = FollowsForm(request.POST)
            if follows_form.is_valid():
                try:
                    user_to_follow = User.objects.get(username=follows_form.cleaned_data['username'])
                    follow = UserFollows(user=request.user, followed_user=user_to_follow)
                    follow.full_clean()
                    follow.save()
                    messages.success(request, f"Vous suivez maintenant {follow.followed_user}.")
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                except User.DoesNotExist:
                    messages.error(request, f"L'utilisateur {follows_form.cleaned_data['username']} n'existe pas.")

    return render(request, 'core/follow.html', context=context)


@login_required
def unfollow_user(request, follows_id):
    UserFollows.objects.get(id=follows_id, user=request.user).delete()
    return redirect('follow')
