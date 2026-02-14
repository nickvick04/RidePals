from django import forms


class RideForm(forms.Form):
  origin = forms.CharField(
    label='Leaving From', 
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., San Fransisco, CA',
      'class': 'form-control'
    })
  )
  
  destination = forms.CharField(
    label='Heading To', 
    max_length=100,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., Los Angeles, CA',
      'class': 'form-control'
    })
  )