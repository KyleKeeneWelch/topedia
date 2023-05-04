# 2101940 Kyle Keene-Welch
# forms.py
# Creates a series of modelforms which use the assigned model to generate fields.

from django.forms import ModelForm
from . models import Room, User, LearningMaterial
from django import forms

# Model form for creating and editing a topic room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['topic', 'host', 'participants', 'learningMaterial']

# Model form for logging in
class LoginForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['email', 'password']

# Model form for registering
class RegisterForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_Confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar', 'password']

# Model form for updating a user account
class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_Confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar', 'password']

# Model form for creating and editing learning material
class MaterialForm(ModelForm):
    class Meta:
        model = LearningMaterial
        fields = '__all__'
        exclude = ['user']