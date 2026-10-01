from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Internship, Application, Certificate
from .forms import RegisterForm, ProfileForm, ApplicationForm

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account created. Please sign in.')
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    role = getattr(getattr(request.user, 'profile', None), 'role', 'student')
    context = {'role':role,'students':Profile.objects.filter(role='student').count(),'internships':Internship.objects.filter(is_active=True).count(),'applications':Application.objects.count(),'selected':Application.objects.filter(status='selected').count(),'pending':Application.objects.filter(status='pending').count(),'certificates':Certificate.objects.count(),'my_apps':Application.objects.filter(student=request.user).select_related('internship','internship__company')}
    return render(request, 'core/dashboard.html', context)

@login_required
def internships(request):
    records = Internship.objects.filter(is_active=True).select_related('company')
    query = request.GET.get('q', '')
    if query:
        records = records.filter(title__icontains=query) | records.filter(skills__icontains=query)
    return render(request, 'core/internships.html', {'internships':records, 'q':query})

@login_required
def apply(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application, created = Application.objects.get_or_create(student=request.user, internship=internship, defaults={'cover_note':form.cleaned_data['cover_note']})
        messages.success(request, 'Application submitted.' if created else 'You already applied for this internship.')
        return redirect('dashboard')
    return render(request, 'core/apply.html', {'internship':internship, 'form':form})

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'core/profile.html', {'form':form})
