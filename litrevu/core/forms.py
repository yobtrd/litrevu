from django import forms
from django.forms import RadioSelect

from core.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=[(i, i) for i in range(6)],
        widget=RadioSelect(),
        coerce=int
    )

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
