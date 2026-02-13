from django import forms


class RideForm(forms.Form):
  search = forms.CharField(
    label='Search by State', 
    max_length=2,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., CA, NY, TX',
      'class': 'form-control'
    })
  )