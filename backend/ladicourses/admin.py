from django.contrib import admin
import logging
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from backend.settings import MEDIA_ROOT, FILEBROWSER_DIRECTORY
from os import path, mkdir, rename
from ladicourses.models import LADICourse, LADILecture

logger = logging.getLogger(__name__)


class CourseAuthorAdmin(admin.ModelAdmin):

    def save_form(self, request, form, change):
        if change:
            course_id = int(request.path[len("/admin/ladicourses/ladicourse/"):request.path.find("/change")])
            old_title = LADICourse.objects.get(id=course_id).title
        else:
            old_title = None
        obj = super().save_form(request, form, change)
        if change and obj.title != old_title:
            CourseAuthorAdmin.update_course_directory(obj, old_title=old_title)
        else:
            # Select automatically the owner
            try:
                obj.owner = request.user
            except AttributeError:
                pass
            # Create the dir if it doesn't exist
            CourseAuthorAdmin.update_course_directory(obj)
        return obj

    def has_change_permission(self, request, obj=None):
        return CourseAuthorAdmin.check_ownership(request, obj)

    def has_delete_permission(self, request, obj=None):
        return CourseAuthorAdmin.check_ownership(request, obj)

    def has_module_permission(self, request):
        return request.user.is_superuser or 'ladicourses.view_ladicourse' in request.user.get_group_permissions()

    @staticmethod
    def check_ownership(request, obj, default_no_owner=True):
        if obj is None or request.user.is_superuser:
            return True
        try:
            owner = obj.professor
        except AttributeError:
            # No owner or the parent is set to None
            return default_no_owner
        return owner == request.user

    @staticmethod
    def update_course_directory(obj, old_title=None):
        course_dir = path.join(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users', str(obj.professor_id), obj.title)
        if not old_title and not path.isdir(course_dir):
            try:
                mkdir(course_dir)
            except OSError:
                logger.warning("Can't create the course folder ({} - prof_id: {})".format(obj.title, obj.professor_id))
            return
        if path.isdir(course_dir):
            logger.warning("Directory with the new course's title already exists, can't rename the old one "
                           "({} - prof_id: {})".format(obj.title, obj.professor_id))
        else:
            try:
                old_path = path.join(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users', str(obj.professor_id), old_title)
                rename(old_path, course_dir)
            except OSError:
                logger.warning("Can't move the course folder ({} - prof_id: {})".format(obj.title, obj.professor_id))


class LectureAuthorAdmin(admin.ModelAdmin):

    def save_form(self, request, form, change):
        if not request.user.is_superuser:
            course_id = request.POST.get('course')
            if not course_id:
                raise SuspiciousOperation("Missing course ID")
            course = LADICourse.objects.get(id=course_id)
            if course.professor != request.user and course.first_assistant != request.user and course.second_assistant != request.user:
                raise PermissionDenied()
        obj = super().save_form(request, form, change)
        return obj

    def has_change_permission(self, request, obj=None):
        return LectureAuthorAdmin.check_ownership(request, obj)

    def has_delete_permission(self, request, obj=None):
        return LectureAuthorAdmin.check_ownership(request, obj)

    def has_module_permission(self, request):
        return request.user.is_superuser or 'ladicourses.view_ladilecture' in request.user.get_group_permissions()

    @staticmethod
    def check_ownership(request, obj):
        if obj is None or request.user.is_superuser:
            return True
        if obj.course.first_assistant == request.user or obj.course.second_assistant == request.user:
            return True
        return obj.course.professor == request.user


admin.site.register(LADICourse, CourseAuthorAdmin)
admin.site.register(LADILecture, LectureAuthorAdmin)
