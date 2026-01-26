from django import forms

class ContactForm(forms.Form):
    name=forms.CharField(label='Name',required=True)
    email=forms.EmailField(label='Email',required=True)
    message=forms.CharField(label='Message',required=True)



from .models import Rental

class RentalForm(forms.ModelForm):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your delivery address (House No., Street, City, Pincode)',
            'rows': 4
        }),
        label='Delivery Address',
        required=True
    )
    
    rental_start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='Start Date & Time'
    )
    
    rental_end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='End Date & Time'
    )
    
    class Meta:
        model = Rental
        fields = ['delivery_address', 'rental_start_date', 'rental_end_date']