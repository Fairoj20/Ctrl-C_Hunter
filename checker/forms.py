from django import forms
from .models import TextEntry

class TextEntryForm(forms.ModelForm):
    class Meta:
        model = TextEntry
        fields = ['title', 'uploaded_file', 'pasted_text']
        widgets = {
            'pasted_text': forms.Textarea(attrs={'rows':6, 'placeholder':'Paste text here...'}),
            'title': forms.TextInput(attrs={'placeholder':'Optional title'}),
        }

    def clean(self):
        cleaned = super().clean()
        file = cleaned.get('uploaded_file')
        text = cleaned.get('pasted_text')
        if not file and not text:
            raise forms.ValidationError("Please upload a text-based file or paste text.")
        return cleaned

class CompareForm(forms.Form):

    entry_a = forms.ModelChoiceField(queryset=TextEntry.objects.all(), required=False)
    entry_b = forms.ModelChoiceField(queryset=TextEntry.objects.all(), required=False)
    pasted_a = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4}))
    pasted_b = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4}))
    file_a = forms.FileField(required=False)
    file_b = forms.FileField(required=False)
