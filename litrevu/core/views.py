from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from core.forms import TicketForm, ReviewForm
from core.models import Ticket, Review


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'core/home.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'core/posts.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def create_ticket(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
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
            return redirect('home')
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

