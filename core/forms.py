from django import forms


ROOM_CHOICES = [
    ('', 'Select a room preference'),
    ('Deluxe Mountain View', 'Deluxe Mountain View'),
    ('Executive Suite', 'Executive Suite'),
    ('Family Room', 'Family Room'),
    ('General Inquiry', 'General Inquiry'),
]


class InquiryForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        error_messages={'required': 'Please share your full name.'},
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Please share an email address.',
            'invalid': 'Please enter a valid email address.',
        },
    )
    phone = forms.CharField(
        max_length=30,
        required=True,
        error_messages={'required': 'Please share a phone / WhatsApp number.'},
    )
    check_in = forms.DateField(required=True, error_messages={'required': 'Please choose a check-in date.'})
    check_out = forms.DateField(required=True, error_messages={'required': 'Please choose a check-out date.'})
    room_preference = forms.ChoiceField(choices=ROOM_CHOICES, required=True)
    adults = forms.IntegerField(required=True, min_value=1, max_value=20)
    children = forms.IntegerField(required=False, min_value=0, max_value=20)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def clean_children(self):
        return self.cleaned_data.get('children') or 0

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError('Check-out date must be after the check-in date.')
        return cleaned_data
