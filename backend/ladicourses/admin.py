from django.contrib import admin
import logging
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpRequest
from backend.settings import MEDIA_ROOT, FILEBROWSER_DIRECTORY
from os import path, makedirs, rename
from ladicourses.models import LADICourse, LADILecture
from typing import Any, Optional
from common.utils import safe_path


logger = logging.getLogger(__name__)


class CourseAuthorAdmin(admin.ModelAdmin):
    """The ModelClass for LADICourse."""


    def save_form(self, request: HttpRequest, form: Any, change: bool) -> LADICourse:
        """This function is called when a user tries to save an object in the Django admin portal."""
        
        obj = super().save_form(request, form, change)
        if change:
            try:
                course_id = int(request.path[len("/admin/ladicourses/ladicourse/"):request.path.find("/change")])
                old_title = LADICourse.objects.get(id=course_id).title
            except ValueError:
                old_title = None
            if obj.title != old_title:
                CourseAuthorAdmin.update_course_directory(obj, old_title=old_title)
                return obj
            
        if not obj.course_site:
            obj.mandatory_redirection = False
            
        # Select automatically the owner
        try:
            obj.owner = request.user
        except AttributeError:
            pass
        # Create the dir if it doesn't exist
        CourseAuthorAdmin.update_course_directory(obj)
        return obj


    def has_change_permission(self, request: HttpRequest, obj: Optional[LADICourse] = None) -> bool:
        """Check if the user is allowed to modify the object in the admin portal."""
        return CourseAuthorAdmin.check_ownership(request, obj)


    def has_delete_permission(self, request: HttpRequest, obj: Optional[LADICourse] = None) -> bool:
        """Check if the user is allowed to delete the object in the admin portal."""
        return CourseAuthorAdmin.check_ownership(request, obj)


    def has_module_permission(self, request: HttpRequest) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return request.user.is_superuser or 'ladicourses.view_ladicourse' in request.user.get_group_permissions()


    @staticmethod
    def check_ownership(request, obj: Optional[LADICourse], default_no_owner: bool = True) -> bool:
        """Check if the user has the ownership in a specific object."""
        if not obj or request.user.is_superuser:
            return True
        try:
            owner = obj.professor
        except AttributeError:
            # No owner or the parent is set to None
            return default_no_owner
        return owner == request.user


    @staticmethod
    def update_course_directory(obj: LADICourse, old_title: Optional[str] = None) -> None:
        """Create or rename a directory for the course material."""
        
        course_dir = safe_path( trusted_part=(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users'),
                                untrusted_part=(str(obj.professor_id), obj.title))
        if not old_title and not path.isdir(course_dir):
            try:
                makedirs(course_dir)
            except OSError:
                logger.warning("Can't create the course folder ({} - prof_id: {})".format(obj.title, obj.professor_id))
            return
        if path.isdir(course_dir):
            logger.warning("Directory with the new course's title already exists, can't rename the old one "
                           "({} - prof_id: {})".format(obj.title, obj.professor_id))
        else:
            try:
                old_path = safe_path(   trusted_part=(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users'),
                                        untrusted_part=(str(obj.professor_id), old_title))
                rename(old_path, course_dir)
            except OSError:
                logger.warning("Can't move the course folder ({} - prof_id: {})".format(obj.title, obj.professor_id))



class LectureAuthorAdmin(admin.ModelAdmin):
    """The ModelClass for LADILecture."""


    def save_form(self, request: HttpRequest, form: Any, change: bool) -> LADILecture:
        """This function is called when a user tries to save an object in the admin portal."""
        
        if not request.user.is_superuser:
            course_id = request.POST.get('course')
            if not course_id:
                raise SuspiciousOperation("Missing course ID")
            course = LADICourse.objects.get(id=course_id)
            if request.user not in { course.professor, course.first_assistant, course.second_assistant }:
                raise PermissionDenied()
        obj = super().save_form(request, form, change)
        return obj


    def has_change_permission(self, request: HttpRequest, obj: Optional[LADILecture] = None) -> bool:
        """Check if the user is allowed to modify the object in the admin portal."""
        return LectureAuthorAdmin.check_ownership(request, obj)


    def has_delete_permission(self, request: HttpRequest, obj: Optional[LADILecture] = None) -> bool:
        """Check if the user is allowed to delete the object in the admin portal."""
        return LectureAuthorAdmin.check_ownership(request, obj)


    def has_module_permission(self, request: HttpRequest) -> bool:
        """Check if the user is allowed to visualize the instances of a specific class in the admin portal."""
        return request.user.is_superuser or 'ladicourses.view_ladilecture' in request.user.get_group_permissions()


    @staticmethod
    def check_ownership(request, obj: Optional[LADILecture]) -> bool:
        """Check if the user has the ownership in a specific object."""
        if not obj or request.user.is_superuser:
            return True
        return request.user in { obj.course.professor, obj.course.first_assistant, obj.course.second_assistant }



admin.site.register(LADICourse, CourseAuthorAdmin)
admin.site.register(LADILecture, LectureAuthorAdmin)
