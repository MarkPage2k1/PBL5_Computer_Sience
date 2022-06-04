from django import forms

from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'name',
            'image',
            'cost',
            'total',
            ]

    name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placehoder' : 'Name'
            }
        )
    )

    image = forms.CharField(
        label='Image',
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
            }
        )
    )

    cost = forms.IntegerField(
        label='Cost',
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
            }
        )
    )

    total = forms.IntegerField(
        label='Total',
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
            }
        )
    )
    
    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        if name:
            self.fields['name'].widget.attrs['readonly'] = True
            return name
        return None