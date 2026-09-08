from django import forms


class PrestamoForm(forms.Form):
    nombre_solicitante = forms.CharField(
        label="Nombre completo",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2'})
    )
    correo_solicitante = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2'})
    )