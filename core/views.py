from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.utils import timezone
from django.urls import reverse_lazy
from .serializers import JobSerializer, ProfileSerializer
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .forms import CustomUserCreationForm, ProfileForm, JobForm
from .models import Profile, Job


class LoginView(AuthLoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile-create')

class LogoutView(AuthLogoutView):
    template_name = "core/logout.html"
    next_page = reverse_lazy("core:login")


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'core/profile_form.html'  
    success_url = reverse_lazy('job-list')  

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user  
        profile.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.profile.exists():  
            return redirect('job-list')
        return context

class JobCreateView(CreateView):
    model = Job
    fields = ['title', 'description', 'skills']  
    template_name = 'core/job_form.html'
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.created_at = timezone.now()  
        return super().form_valid(form)

class JobListView(ListView):
    model = Job
    template_name = 'core/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10  


class JobAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class ProfileAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('core:job_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def profile_update(request):
    
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:profile_update')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})


class JobDetailView(DetailView):
    model = Job
    template_name = 'core/job_detail.html'
    context_object_name = 'job'

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('core:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'core/job_form.html', {'form': form})