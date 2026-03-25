from django import forms

from core.models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
            'rating': 'Note'
            }


class FollowsForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur')
