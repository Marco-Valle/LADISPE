from django.contrib import admin
from django.core.exceptions import PermissionDenied
from ladicontent.models import LADIForm, LADINews, LADIStory
from ladicontent.models import LADIGallery, LADIPicture
from ladicontent.models import LADIStaff

nested_ownership = {
    # Define nested ownership here
    LADIPicture: lambda obj: obj.gallery.owner,
    LADIStaff: lambda obj: obj.user,
}


class AuthorAdmin(admin.ModelAdmin):

    # exclude = ('owner',)

    def save_form(self, request, form, change):
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

    def has_change_permission(self, request, obj=None):
        return AuthorAdmin.check_ownership(request, obj)

    def has_delete_permission(self, request, obj=None):
        return AuthorAdmin.check_ownership(request, obj)

    @staticmethod
    def check_ownership(request, obj, default_no_owner=True):
        if obj is None or request.user.is_superuser:
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
    def check_model_permission(obj, user):
        return user.is_superuser or 'ladicontent.view_{}'.format(obj.__name__.lower()) in user.get_group_permissions()


class NewsAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADINews, request.user)


class GalleryAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADIGallery, request.user)


class PictureAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADIPicture, request.user)


class StoryAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADIStory, request.user)


class StaffAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADIStaff, request.user)


class FormAuthorAdmin(AuthorAdmin):

    def has_module_permission(self, request):
        return AuthorAdmin.check_model_permission(LADIForm, request.user)


admin.site.register(LADINews, NewsAuthorAdmin)
admin.site.register(LADIGallery, GalleryAuthorAdmin)
admin.site.register(LADIPicture, PictureAuthorAdmin)
admin.site.register(LADIStory, StoryAuthorAdmin)
admin.site.register(LADIStaff, StaffAuthorAdmin)
admin.site.register(LADIForm, FormAuthorAdmin)
