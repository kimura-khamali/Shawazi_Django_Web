from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('lawyer', 'Lawyer')])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['phone_number']
        # user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user







