from django.db import models
from django.core.exceptions import ValidationError
from courses.models import Subject


class Exam(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('retake', 'Retake'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    room = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.subject.name} - {self.date}"

    def clean(self):
        if self.notes and len(self.notes.strip()) == 1:
            raise ValidationError({'notes': 'Notes are too short to be useful.'})
