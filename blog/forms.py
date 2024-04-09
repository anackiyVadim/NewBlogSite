from django import forms

from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Post, Comment, Subscribe, PostPhoto


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'links']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'links': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }


class PostPhotoForm(forms.ModelForm):
    class Meta:
        model = PostPhoto
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


PostPhotoFormSet = inlineformset_factory(Post, PostPhoto, form=PostPhotoForm, extra=3)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'published_date', 'post')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        exclude = ()


class CombinedForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    avatar = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CombinedForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].initial = self.instance.profile.date_of_birth
        self.fields['bio'].initial = self.instance.profile.bio
        self.fields['avatar'].initial = self.instance.profile.avatar

    def save(self, commit=True):
        user = super(CombinedForm, self).save(commit=False)
        profile = user.profile
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.bio = self.cleaned_data['bio']
        profile.avatar = self.cleaned_data['avatar']
        if commit:
            user.save()
            profile.save()
        return user


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
