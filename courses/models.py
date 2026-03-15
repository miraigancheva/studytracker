from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Subject(models.Model):
    name = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    credits = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    semester = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.semester and len(self.semester.strip()) < 2:
            raise ValidationError({'semester': 'Please enter a valid semester name.'})
        if self.name and len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Subject name is too short.'})


class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='groups')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
