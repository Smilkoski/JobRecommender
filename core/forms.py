from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Job, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['skills', 'resume']
#         widgets = {
#             'skills': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter skills as comma-separated: Python, Django, ML'}),
#         }
#
#     def clean_resume(self):
#         resume = self.cleaned_data.get('resume')
#         if resume:
#             if not resume.name.lower().endswith('.pdf'):
#                 raise forms.ValidationError('Upload must be a PDF file only.')
#             if resume.size > 15 * 1024 * 1024:
#                 raise forms.ValidationError('Resume size must be under 15MB.')
#         return resume


class ProfileForm(forms.ModelForm):
    
    skills_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Comma-separated skills, e.g. Python,Django,SQL'
    )


    class Meta:
        model = Profile
        fields = ('resume',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.skills:
            self.fields['skills_text'].initial = ','.join(self.instance.skills)


    def clean_skills_text(self):
        text = self.cleaned_data.get('skills_text', '')
        if not text:
            return []
            
        return [s.strip() for s in text.split(',') if s.strip()]


    def save(self, commit=True):
        instance = super().save(commit=False)
        skills_list = self.cleaned_data.get('skills_text', [])
        instance.skills = skills_list
        if commit:
            instance.save()
        return instance


class JobForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


    class Meta:
        model = Job
        fields = ('title', 'description', 'skills')