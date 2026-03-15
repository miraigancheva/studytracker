from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'date', 'room', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'room': forms.TextInput(attrs={'placeholder': 'e.g. H20 or online'}),
        }
        labels = {
            'room': 'Room / Location',
        }
        help_texts = {
            'notes': 'Topics to revise, allowed materials, etc.',
        }

    def clean_notes(self):
        notes = self.cleaned_data.get('notes', '').strip()
        if notes and len(notes) < 3:
            raise forms.ValidationError('Notes are too short — write something useful or leave it empty.')
        return notes


class ExamStatusForm(forms.ModelForm):
    subject_display = forms.CharField(
        label='Subject',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    date_display = forms.CharField(
        label='Date',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )

    class Meta:
        model = Exam
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['subject_display'].initial = self.instance.subject.name
            self.fields['date_display'].initial = str(self.instance.date)
        self.order_fields(['subject_display', 'date_display', 'status'])
