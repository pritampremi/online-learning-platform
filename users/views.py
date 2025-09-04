from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('users:login')


@login_required
def home_view(request):
    is_instructor = False
    is_student = False

    if request.user.is_authenticated:
        is_instructor = getattr(request.user, 'is_instructor', False)
        is_student = getattr(request.user, 'is_student', False)

    return render(request, 'users/home.html', {
        'is_instructor': is_instructor,
        'is_student': is_student,
    })

