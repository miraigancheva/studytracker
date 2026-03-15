from django import forms
from .models import Subject, StudyGroup


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'professor', 'credits', 'semester', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'semester': forms.TextInput(attrs={'placeholder': 'e.g. Winter 2024/25'}),
        }
        labels = {
            'professor': 'Professor name',
            'credits': 'ECTS credits',
        }
        help_texts = {
            'credits': 'How many credits is this subject worth?',
            'semester': 'Which semester are you taking this in?',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Subject name is too short.')
        return name

    def clean_credits(self):
        c = self.cleaned_data['credits']
        if c < 1 or c > 30:
            raise forms.ValidationError('Credits must be between 1 and 30.')
        return c

    def clean_semester(self):
        semester = self.cleaned_data['semester'].strip()
        if len(semester) < 2:
            raise forms.ValidationError('Please enter a valid semester name.')
        return semester


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'subjects', 'description']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'subjects': 'Which subjects does this group cover?',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters.')
        return name
