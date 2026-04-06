from core.widgets import FormWidgetMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(FormWidgetMixin, UserCreationForm):
    """Custom registration form with password confirmation placeholder."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Confirmer mot de passe",
            }
        )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "password1", "password2")
