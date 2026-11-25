from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profil

class CustomUserCreationForm(UserCreationForm):
    strada = forms.CharField(max_length=255, required=False, label="Strada")
    data_nasterii = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Data nasterii")
    bio = forms.CharField(required=False, widget=forms.Textarea, label="Despre mine")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'telefon', 'tara', 'judet')

    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if telefon:
            if not telefon.isdigit() or len(telefon) != 10 or not telefon.startswith('07'):
                raise forms.ValidationError("Numarul de telefon trebuie sa contina exact 10 cifre si sa incepa cu '07'.")
        return telefon

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(('@gmail.com', '@yahoo.com', '@outlook.com')):
            raise forms.ValidationError("Va rugam sa folositi o adresa de email valida (Gmail, Yahoo, Outlook).")
        return email

    def clean_first_name(self):
        nume = self.cleaned_data.get('first_name')
        if nume and not nume[0].isupper():
            raise forms.ValidationError("Numele trebuie sa incepa cu litera mare.")
        return nume

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    tine_minte = forms.BooleanField(
        required=False, 
        initial=False, 
        label='Tine-ma minte timp de o zi'
    )    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'telefon', 'tara', 'judet')

class ProfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ('strada', 'data_nasterii', 'bio')
        widgets = {
            'data_nasterii': forms.DateInput(attrs={'type': 'date'}),
        }