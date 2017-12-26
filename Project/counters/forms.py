from django import forms


class FileFieldForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'file'})
    )
    #id = forms.CharField(max_length=9, widget=forms.HiddenInput())
