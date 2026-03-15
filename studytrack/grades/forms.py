from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    # read-only display fields
    subject_display = forms.CharField(
        label='Subject (cannot change)',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )

    class Meta:
        model = Grade
        fields = ['subject', 'score', 'max_score', 'date', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes...'}),
            'score': forms.NumberInput(attrs={'step': '0.5', 'min': '0'}),
            'max_score': forms.NumberInput(attrs={'step': '0.5', 'min': '1'}),
        }
        labels = {
            'score': 'Your score',
            'max_score': 'Out of',
            'comment': 'Notes (optional)',
        }
        help_texts = {
            'score': 'The points you got.',
            'max_score': 'Total points possible.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['subject_display'].initial = str(self.instance.subject)
        else:
            # hide the read-only field on create since there's nothing to show yet
            self.fields.pop('subject_display')

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        max_score = cleaned_data.get('max_score')
        if score is not None and max_score is not None:
            if score > max_score:
                raise forms.ValidationError('Your score cannot be higher than the maximum score.')
        return cleaned_data
