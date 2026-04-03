from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms import SignUpForm


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a bien été créé, vous pouvez à présent vous connecter.")
            return redirect('login')
    return render(request, 'accounts/signup.html', context={'form': form})
