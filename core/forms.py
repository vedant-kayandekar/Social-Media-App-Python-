from django import forms
from . models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_body', 'commenter_name']
        widgets = {
            'commenter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment_body': forms.Textarea(attrs={'class': 'form-control'}),
        }