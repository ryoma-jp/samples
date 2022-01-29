from django import forms

from app.models import TableItems, SelectFormItems, UploadFiles

class TableItemsForm(forms.ModelForm):
    class Meta:
        model = TableItems
        fields = ('first', 'last', 'handle',)

class SelectFormItemsForm(forms.ModelForm):
    class Meta:
        model = SelectFormItems
        fields = ('item_name',)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFiles
        fields = ('description', 'upload_file', )
