from django import forms

from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'name',
            'cost',
            'count',
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

    cost = forms.IntegerField(
        label='Cost',
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
            }
        )
    )

    count = forms.IntegerField(
        label='Count',
        initial=0,
        widget=forms.NumberInput(
            attrs={
                'class' : 'form-control',
            }
        )
    )
    
    # Đa năng hóa lại contrustor
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['name'].widget.attrs['readonly'] = True
