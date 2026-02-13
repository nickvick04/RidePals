from django import forms


class RideForm(forms.Form):
  search = forms.CharField(
    label='Search by State', 
    max_length=2,  # Changed from 64 to 2 for state abbreviations
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., CA, NY, TX',
      'class': 'form-control'  # Optional: Bootstrap styling
    })
  )