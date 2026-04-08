from accounts.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render


class CustomLoginView(LoginView):
    """Login view with placeholder labels."""

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update(
                {
                    "title": "Veuillez remplir ce champ",
                    "aria-label": field.label,
                    "placeholder": field.label,
                    "class": "input mb-2",
                }
            )
            field.label = ""
            field.help_text = None
        return form


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
