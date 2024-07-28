# forms.py

from django import forms
from .models import CustomUser,WasteIssue,PickupRequest,UserImage

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    user_role = forms.ChoiceField(choices=[('customer', 'Customer'), ('admin', 'Admin')])

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'user_role']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = self.cleaned_data["user_role"] == 'admin'
        if commit:
            user.save()
        return user
class ReportIssueForm(forms.ModelForm):
    class Meta:
        model = WasteIssue
        fields = ['issue_type', 'description', 'location']
class RequestPickupForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['item_description', 'location']
class AddImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']        
class UpdateIssueForm(forms.ModelForm):
    class Meta:
        model = WasteIssue
        fields = ['status']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = 'New Status' 