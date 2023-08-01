from django import forms
from Users.models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean_national_code(self):
        if len(self.cleaned_data["national_code"]) == 10:
            return self.cleaned_data["national_code"]
        raise ValidationError("Length should be exactly 10")
    
    def clean_full_name(self):
        data = self.cleaned_data["full_name"]
        if len(data.split(' ')) == 2:
            first_name, last_name = data.split(' ')
            if first_name == first_name.title() and last_name == last_name.title():
                return data
        raise ValidationError("Full Name is not clean")
