from django import forms
from .models import UserRegistration, NGO, EventRegistration

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input-field'}), required=True)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'input-field'}), required=True)

    class Meta:
        model = UserRegistration
        fields = ['first_name', 'last_name', 'contact_number', 'address', 'gender', 'age', 'interests', 'medical_details', 'username', 'password']

class NGORegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input-field'}), required=True)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'input-field'}), required=True)

    class Meta:
        model = NGO
        fields = ['organization_name', 'contact_person', 'contact_email', 'contact_number', 'organization_address', 'registration_number', 'establishment_year', 'area_of_focus', 'additional_comments', 'username', 'password']

# New EventRegistrationForm
class EventRegistrationForm(forms.ModelForm):
    # Add a new field for the specific date
    specific_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
        required=True,
        label="Specific Date"
    )

    class Meta:
        model = EventRegistration
        fields = ['first_name', 'last_name', 'contact_number', 'address', 'gender', 'age', 'event', 'specific_date']
