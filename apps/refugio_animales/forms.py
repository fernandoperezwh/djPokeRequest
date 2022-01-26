# coding=utf-8
# django packages
from django import forms


class DjRefugioAnimalesLoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class DjRefugioAnimalesVacunaForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre de la vacuna",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class DjRefugioAnimalesPersonaForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre(s)",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellidos = forms.CharField(
        label="Apellidos",
        max_length=70,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    edad = forms.IntegerField(
        label="Edad",
        min_value=10,
        max_value=150,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Número de teléfono",
        min_length=8,
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo electronico de contacto",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    domicilio = forms.CharField(
        label="Dirección completa del domicilio",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
