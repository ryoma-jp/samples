from django import forms

from app.models import TableItems, SelectFormItems, UploadFiles, ImageGallery, GraphSignalSelector

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

class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = ImageGallery
        fields = ('images_per_page',)

class GraphSignalSelectorForm(forms.ModelForm):
    class Meta:
        model = GraphSignalSelector
        fields = ('signal',)



