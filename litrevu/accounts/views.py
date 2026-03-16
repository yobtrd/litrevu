from django.shortcuts import redirect, render

from . import forms


def signup(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print("Votre compte a été enregistré")
            return redirect('login')
    return render(request, 'accounts/signup.html', context={'form': form})
