from django import forms

from django.contrib.auth.models import User
from socialnetwork.models import Profile

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class CreatePost(forms.Form):
    post = forms.CharField(max_length=500)
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)


#
class GlobalPostForm(forms.Form):
    post = forms.CharField(max_length=500)
    last_name     = forms.CharField(max_length=20)
    first_name    = forms.CharField(max_length=20)
#     birthday      = forms.DateField(required=False)
#     address       = forms.CharField(required=False, max_length=200)
#     city          = forms.CharField(required=False, max_length=30)
#     state         = forms.CharField(required=False, max_length=20)
#     zip_code      = forms.CharField(required=False, max_length=10)
#     country       = forms.CharField(required=False, max_length=30)
#     email         = forms.CharField(required=False, max_length=32)
#     home_phone    = forms.CharField(required=False, max_length=16)
#     cell_phone    = forms.CharField(required=False, max_length=16)
#     fax           = forms.CharField(required=False, max_length=16)
#     spouse_last   = forms.CharField(required=False, max_length=16)
#     spouse_first  = forms.CharField(required=False, max_length=16)
#     spouse_birth  = forms.DateField(required=False)
#     spouse_cell   = forms.CharField(required=False, max_length=16)
#     spouse_email  = forms.

MAX_UPLOAD_SIZE = 2500000

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'bio', 'img']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['first_name'] = instance.first_name
            self.initial['last_name'] = instance.last_name
            self.initial['username'] = instance.username
            self.initial['bio'] = instance.bio
            self.initial['img'] = instance.img
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = True


    def __unicode__(self):
        return self.user.get_full_name()

    def clean_picture(self):
        img = self.cleaned_data['img']
        if not img:
            raise forms.ValidationError('You must upload a picture')
        if not img.content_type or not img.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if img.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return img



class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'bio', 'img']






