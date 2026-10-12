from django import forms
from .models import StudySession


class SessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['topic', 'date', 'start', 'end', 'repeat', 'remind']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}),
                   'start': forms.TimeInput(attrs={'type': 'time'}),
                   'end': forms.TimeInput(attrs={'type': 'time'})}

    def clean(self):
        d = super().clean()
        if d.get('start') and d.get('end') and d['end'] <= d['start']:
            raise forms.ValidationError('End time must be after start time.')
        return d
