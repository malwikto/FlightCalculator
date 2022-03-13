from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ChoiceField, CharField, Textarea, ImageField

from accounts.models import Profile
from datetime import date


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name']

    def save(self, commit=True):
        result = super(SignUpForm, self).save(commit)
        profile = Profile(id=result.id, first_name='', last_name='', dob=None, user=result)
        if commit:
            profile.save()
        return result

class UserProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'


# class UserProfileUpdateForm(ModelForm):
#
#
#     class Meta:
#         model = Profile
#         fields = '__all__'
#
#     profile_picture = ImageField(default="default.jpg", upload_to="profile_pics")
#     first_name = CharField()
#     last_name = CharField()
