from django import forms
from models import User


class InvitationForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Email Address of Friend to invite.', 'class':'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter Username.', 'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter email address', 'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Enter Password', 'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'size': 32, 'placeholder': 'Confirm Password', 'class':'form-control'}))

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(" Confirm Password Did not match.")


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(widget=forms.TextInput, label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']