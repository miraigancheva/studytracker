from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from courses.models import Subject


class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_score = models.FloatField(default=100, validators=[MinValueValidator(1)])
    date = models.DateField()
    comment = models.TextField(blank=True)

    def percentage(self):
        return round((self.score / self.max_score) * 100, 1)

    def passed(self):
        return self.percentage() >= 50

    def letter(self):
        p = self.percentage()
        if p >= 90:
            return 'A'
        elif p >= 75:
            return 'B'
        elif p >= 60:
            return 'C'
        elif p >= 50:
            return 'D'
        return 'F'

    def clean(self):
        if self.score is not None and self.max_score is not None:
            if self.score > self.max_score:
                raise ValidationError('Score cannot be higher than the maximum score.')

    def __str__(self):
        return f"{self.subject.name} - {self.score}/{self.max_score}"

    class Meta:
        ordering = ['-date']
