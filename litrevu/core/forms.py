from core.models import Review, Ticket
from core.widgets import FormWidgetMixin
from django import forms
from django.forms import RadioSelect


class CustomImageInput(forms.ClearableFileInput):
    """Custom template for image input."""

    template_name = "widgets/custom_image_input.html"


class TicketForm(forms.ModelForm):
    """Form for creating/editing tickets with translated labels."""

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
            "title": "Titre",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "title-field"}),
            "description": forms.Textarea(attrs={"class": "body-field"}),
            "image": CustomImageInput(attrs={"class": "image-input"}),
        }


class ReviewForm(forms.ModelForm):
    """Review form with radio button rating selector."""

    rating = forms.TypedChoiceField(
        choices=[(i, i) for i in range(1, 6)], widget=RadioSelect(), coerce=int
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "body": "Commentaire", "rating": "Note"}
        widgets = {
            "headline": forms.TextInput(attrs={"class": "title-field"}),
            "body": forms.Textarea(attrs={"class": "body-field"}),
        }


class FollowsForm(FormWidgetMixin, forms.Form):
    """Simplified username input form for following users."""

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "id": "search_user",
            }
        ),
    )
