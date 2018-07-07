from django import forms

from picture_list.models import Item

MAX_UPLOAD_SIZE = 2500000

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ( 'picture', 'text')

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture
