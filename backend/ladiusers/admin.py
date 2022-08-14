from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import LADIUser


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=LADIUser.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = LADIUser
    list_display = ('email', 'name', 'surname', 'active', 'superuser', 'staff', 'is_professor', 'is_borsista')
    list_filter = ('email', 'active', 'superuser', 'staff')
    fieldsets = (
        (None, {'fields': ('name', 'surname', 'email', 'password', )}),
        ('Permissions', {'fields': ('active', 'superuser', 'staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'surname', 'email', 'password1', 'password2', 'active', 'superuser', 'staff')}
         ),
    )
    search_fields = ('email',)
    readonly_fields = ('is_professor', 'is_borsista')
    ordering = ('email', 'name', 'surname')

    def save_form(self, request, form, change):
        if not request.user.is_superuser:
            try:
                post_email = request.POST.get('email', None)
                post_superuser = request.POST.get('superuser', 'off')
                if not post_email:
                    raise ObjectDoesNotExist()
                old_user_istance = LADIUser.objects.get(email=post_email)
                if old_user_istance.is_superuser or post_superuser == 'on':
                    raise SuspiciousOperation("Only superadmins can modify superadmins")
            except ObjectDoesNotExist:
                if post_superuser == 'on':
                    raise SuspiciousOperation("Only superadmins can add superadmins")
        obj = super().save_form(request, form, change)
        return obj


admin.site.register(LADIUser, CustomUserAdmin)

# Unregister the original Group admin.
admin.site.unregister(Group)

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)
