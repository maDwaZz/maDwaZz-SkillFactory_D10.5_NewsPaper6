from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("title")

        if name == description:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
