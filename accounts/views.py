from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from checker.models import TextEntry, ComparisonHistory


def register_view(request):
    """User registration with role and institution"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            institution = form.cleaned_data['institution']
            phone = form.cleaned_data['phone']
            profile = user.profile  # created by signal
            profile.role = role
            profile.institution = institution
            profile.phone = phone
            profile.save()

            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('checker:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('checker:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """View and update user profile"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    """User dashboard with activity summary"""
    user_entries = TextEntry.objects.filter(user=request.user)
    comparisons = ComparisonHistory.objects.filter(
        source_a_entry__user=request.user
    ) | ComparisonHistory.objects.filter(
        source_b_entry__user=request.user
    )

    context = {
        'user': request.user,
        'entry_count': user_entries.count(),
        'comparison_count': comparisons.count(),
        'last_comparison': comparisons.order_by('-compared_at').first()
    }
    return render(request, 'accounts/dashboard.html', context)