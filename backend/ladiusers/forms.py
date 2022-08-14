from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import LADIUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = LADIUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = LADIUser
        fields = ('email',)
