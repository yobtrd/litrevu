from accounts.forms import SignUpForm
from core.widgets import FormWidgetMixin
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


class CustomAuthenticationForm(FormWidgetMixin, AuthenticationForm):
    """Login view with standardized widget styling."""

    pass


class CustomLoginView(LoginView):
    """Form that automatically applies our widget standards."""

    form_class = CustomAuthenticationForm


def signup(request):
    """Handle user registration with:
    - GET: Empty signup form
    - POST: Form validation and account creation
    - Success: Redirect to login with confirmation message
    """
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Votre compte a bien été créé, vous pouvez à présent vous connecter.",
            )
            return redirect("login")
    return render(request, "accounts/signup.html", context={"form": form})
