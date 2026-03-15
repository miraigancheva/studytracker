from django.contrib import admin
from .models import Subject, StudyGroup

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'professor', 'semester', 'credits']

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['subjects']
