from django.contrib import admin
from .models import Exam

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['subject', 'date', 'status', 'room']
    list_filter = ['status']
