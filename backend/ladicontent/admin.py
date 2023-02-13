from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from typing import Any, Union, Optional
from ladiusers.models import LADIUser
from ladicontent.models import LADIForm, LADINews, LADIStory
from ladicontent.models import LADIGallery, LADIPicture
from ladicontent.models import LADIStaff


nested_ownership = {
    # Define nested ownership here
    LADIPicture: lambda obj: obj.gallery.owner,
    LADIStaff: lambda obj: obj.user,
}


class AuthorAdmin(admin.ModelAdmin):
    """The class used to manage the admin page permissions for LADIContent, based on ownership."""


    def save_form(self, request: HttpRequest, form: Any, change: bool
                  ) -> Union[LADIForm, LADINews, LADIStory, LADIGallery, LADIPicture, LADIStaff]:
        """This function is called when a user tries to save an object in the Django admin portal."""
        
        obj = super().save_form(request, form, change)
        if not request.user.is_superuser and type(obj) == LADIPicture:
            # Protect against not allowed Home modifications
            gallery_id = request.POST.get("gallery")
            if gallery_id and LADIGallery.objects.get(pk=gallery_id).title == 'Home':
                raise PermissionDenied()
        # Select automatically the owner
        if not change:
            try:
                obj.owner = request.user
            except AttributeError:
                pass
        return obj


    def has_change_permission(self,
                              request: HttpRequest,
                              obj: Optional[Union[LADIForm, LADINews, LADIStory, LADIGallery, LADIPicture, LADIStaff]] = None
                              ) -> bool:
        """Check if the user is allowed to modify the object in the admin portal."""
        return AuthorAdmin.check_ownership(request, obj)


    def has_delete_permission(self,
                              request: HttpRequest,
                              obj: Optional[Union[LADIForm, LADINews, LADIStory, LADIGallery, LADIPicture, LADIStaff]] = None
                              ) -> bool:
        """Check if the user is allowed to delete the object in the admin portal."""
        return AuthorAdmin.check_ownership(request, obj)


    @staticmethod
    def check_ownership(request: HttpRequest,
                        obj: Union[LADIForm, LADINews, LADIStory, LADIGallery, LADIPicture, LADIStaff],
                        default_no_owner: bool = True) -> bool:
        """Check if the user has the ownership in a specific object."""
        
        if not obj or request.user.is_superuser:
            return True
        try:
            if type(obj) in nested_ownership:
                owner = nested_ownership[type(obj)](obj)
            else:
                owner = obj.owner
        except AttributeError:
            # No owner or the parent is set to None (for the nested ownership)
            return default_no_owner
        return owner == request.user


    @staticmethod
    def check_model_permission(obj: Union[LADIForm, LADINews, LADIStory, LADIGallery, LADIPicture, LADIStaff], user: LADIUser) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return user.is_superuser or 'ladicontent.view_{}'.format(obj.__name__.lower()) in user.get_group_permissions()



class NewsAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADINews, based on ownership."""

    def has_module_permission(self, request):
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADINews, request.user)



class GalleryAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADIGallery, based on ownership."""

    def has_module_permission(self, request):
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADIGallery, request.user)



class PictureAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADIPicture, based on ownership."""

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADIPicture, request.user)



class StoryAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADIStory, based on ownership."""

    def has_module_permission(self, request):
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADIStory, request.user)



class StaffAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADIStaff, based on ownership."""

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADIStaff, request.user)



class FormAuthorAdmin(AuthorAdmin):
    """The class used to manage the admin page permissions for LADIForm, based on ownership."""

    def has_module_permission(self, request: HttpRequest) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return AuthorAdmin.check_model_permission(LADIForm, request.user)



admin.site.register(LADINews, NewsAuthorAdmin)
admin.site.register(LADIGallery, GalleryAuthorAdmin)
admin.site.register(LADIPicture, PictureAuthorAdmin)
admin.site.register(LADIStory, StoryAuthorAdmin)
admin.site.register(LADIStaff, StaffAuthorAdmin)
admin.site.register(LADIForm, FormAuthorAdmin)
