from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Author, Feature_selection



class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This already exists;)'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class edit_profile(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('username', 'email', 'profile_pic')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            author = Author.objects.exclude(pk=self.instance.pk).get(email=email)
        except Author.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.' )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            author = Author.objects.exclude(pk=self.instance.pk).get(username=username)
        except Author.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.')

    def save(self, commit=True):
        author = super(edit_profile, self).save(commit=False)
        author.username = self.cleaned_data['username']
        author.email = self.cleaned_data['email']
        author.profile_pic = self.cleaned_data['profile_pic']
        if commit:
            author.save()
        return author


class FeatureSelectionForm(forms.ModelForm):
    class Meta:
        model = Feature_selection
        fields = ['task_name','isExternal', 'splitRatio', 'rankingAlgorithm','vipComponent', 'rocType', 'tupaType', 'isMotabo', 'scaleType', 'iterations', 'survivalRate', 'motaboFile', 'sample_file', 'class_file', 'sampleName_file', 'variableName_file', 'sent_email']
