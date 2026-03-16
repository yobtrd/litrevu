from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View


class SignUpForm(UserCreationForm, View):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
