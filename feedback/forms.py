from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback']
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'您的稱呼...'}),
            'email':forms.TextInput(attrs={'placeholder':'您的電子郵件...'}),
            'feedback': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': '請輸入訊息...'})
        }
