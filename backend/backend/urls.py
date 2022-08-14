from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site

from ladiusers.views import get_user

from ladicontent.views import get_news, get_news_count
from ladicontent.views import get_pictures, get_pictures_count
from ladicontent.views import get_stories, get_stories_count
from ladicontent.views import get_galleries, get_galleries_count, get_gallery_pictures
from ladicontent.views import get_staffs, get_staffs_count
from ladicontent.views import get_forms, get_forms_count
from ladicourses.views import get_courses, get_courses_count, get_courses_materials, get_courses_lectures
from ladicourses.views import get_lectures, get_lectures_count

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('api/ladiuser/', get_user),
    path('api/ladinews/', get_news),
    path('api/ladinews/count/', get_news_count),
    path('api/ladipictures/', get_pictures),
    path('api/ladipictures/count/', get_pictures_count),
    path('api/ladistories/', get_stories),
    path('api/ladistories/count/', get_stories_count),
    path('api/ladigalleries/', get_galleries),
    path('api/ladigalleries/count/', get_galleries_count),
    path('api/ladigalleries/pictures/', get_gallery_pictures),
    path('api/ladistaffs/', get_staffs),
    path('api/ladistaffs/count/', get_staffs_count),
    path('api/ladiforms/', get_forms),
    path('api/ladiforms/count/', get_forms_count),
    path('api/ladicourses/', get_courses),
    path('api/ladicourses/count/', get_courses_count),
    path('api/ladicourses/materials/', get_courses_materials),
    path('api/ladicourses/lectures/', get_courses_lectures),
    path('api/ladilectures/', get_lectures),
    path('api/ladilectures/count/', get_lectures_count),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'LADIAdmin'
