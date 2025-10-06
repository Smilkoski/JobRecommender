from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100)
    date_registered = models.DateTimeField(default=datetime.utcnow)
    last_login = models.DateTimeField(default=datetime.utcnow)
    linkedin_url = models.CharField(max_length=150, blank=True)
    github_url = models.CharField(max_length=150, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.JSONField(default=list)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.ManyToManyField(Tag, blank=True)  # Allows jobs without skills
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Profile)
def parse_resume_on_save(sender, instance, created, **kwargs):
    if instance.resume and (created or not hasattr(instance, '_resume_parsed')):
        print(f"Parsing resume for {instance.user.username}...")
        instance._resume_parsed = True  # Avoid re-parsing on updates