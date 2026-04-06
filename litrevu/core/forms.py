from core.models import Review, Ticket
from core.widgets import FormWidgetMixin
from django import forms
from django.forms import RadioSelect


class TicketForm(forms.ModelForm):
    """Form for creating/editing tickets with translated labels."""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
            "title": "Titre",
        }


class ReviewForm(forms.ModelForm):
    """Review form with radio button rating selector."""

    rating = forms.TypedChoiceField(
        choices=[(i, i) for i in range(6)], widget=RadioSelect(), coerce=int
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "body": "Commentaire", "rating": "Note"}


class FollowsForm(FormWidgetMixin, forms.Form):
    """Simplified username input form for following users."""

    username = forms.CharField(label="Nom d'utilisateur")
