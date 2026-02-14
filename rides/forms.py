from django import forms


class RideForm(forms.Form):
  origin_state = forms.CharField(
    label='Leaving From (State)', 
    max_length=2,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., CA, NY, TX',
      'class': 'form-control'
    })
  )
  
  destination_state = forms.CharField(
    label='Heading To (State)', 
    max_length=2,
    required=False,
    widget=forms.TextInput(attrs={
      'placeholder': 'e.g., CA, NY, TX',
      'class': 'form-control'
    })
  )