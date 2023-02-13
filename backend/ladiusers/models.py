from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from ladiusers.managers import CustomUserManager
from typing import Any


class LADIUser(AbstractBaseUser, PermissionsMixin):
    """LADIUSer db model """
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text="""
        REMARKS:<br>
        * in order to make <b>IS_BORSISTA</b> true for a user the group <b>Borsisti</b> should be created and he has to be added;<br>
        * in order to make <b>IS_PROFESSOR</b> true for a user the group <b>Professors</b> should be created and he has to be added.
        """
    )
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False, help_text="Required for the admin page.")      # an admin user; non super-user
    superuser = models.BooleanField(default=False, help_text="Only superusers can add or change superusers.")

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []                # Email & Password are required by default.
    objects = CustomUserManager()


    def get_full_name(self) -> str:
        """Get the firstname and the surname of the user together."""
        return '{} {}'.format(self.name, self.surname)


    def get_short_name(self) -> str:
        """Get the surname of the user."""
        return self.surname


    def __str__(self) -> str:
        """String representation of LADIUser."""
        return '{} {} - {}'.format(self.name, self.surname, self.email)


    def has_perm(self, perm: str, obj: Any = None) -> bool:
        """Check if the user has a specific permission checking the groups policies."""
        return self.active and (self.superuser or (self.staff and perm in self.get_group_permissions()))


    def has_module_perms(self, app_label: str) -> bool:
        """Check if the user is allowed to see the app_label for a specific class in the admin page."""
        return True


    @property
    def is_professor(self) -> bool:
        """Property: if user is a professor."""
        return self.groups.filter(name='Professors').exists()


    @property
    def is_borsista(self) -> bool:
        """Property: if user is a borsista (intern)."""
        return self.groups.filter(name='Borsisti').exists()


    @property
    def is_staff(self) -> bool:
        """Property: if user is staff (he has access to the admin page)."""
        return self.staff


    @property
    def is_superuser(self) -> bool:
        """Property: if user is a superuser (admin)."""
        return self.superuser
