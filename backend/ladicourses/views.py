from common.database import Database
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ObjectDoesNotExist
from backend.settings import MEDIA_ROOT, MEDIA_URL, FILEBROWSER_DIRECTORY, MAX_DEPTH_IN_MATERIAL_SEARCH
from os import path, walk
from urllib.parse import quote
from time import strftime, localtime
from filebrowser.base import FileObject

from ladicourses.models import LADICourse, LADILecture

database_search_rules = {
    LADICourse: lambda params: courses_retrieve_results(params),
    LADILecture: lambda params: lectures_retrieve_results(params),
}

db = Database(database_search_rules)
mandatory_attributes = lambda request: [] if request.user.is_superuser else ['public']  
material_empty_response = JsonResponse([{'title': '', 'breadcrumbs': [], 'files': []}], safe=False)


# LADICourse

def get_courses(request):
    return db.database_search(request, LADICourse, default_attributes=mandatory_attributes(request))


def get_courses_count(request):
    return db.database_rows_count(request, LADICourse, default_attributes=mandatory_attributes(request))


def get_courses_lectures(request):
    course = db.get_parent(request, LADICourse)
    if not course:
        return JsonResponse([], safe=False)
    if not course.public and not request.user.is_superuser:
        if request.user != course.professor and request.user != course.first_assistant and request.user != course.second_assistant:
            return JsonResponse([], safe=False)
    query_set = LADILecture.objects.filter(course_id=course.id)
    query_set = query_set.order_by('timestamp').reverse()
    data = list(query_set.values())
    for idx, result in enumerate(data):
        # Remove unused large field
        del(data[idx]['html'])
        for key, value in result.items():
            # Check for not serializable FileObjects
            if type(value) == FileObject:
                data[idx][key] = value.path
    return JsonResponse(data, safe=False)


def get_courses_materials(request):
    params = Database.get_request(request)
    try:
        if 'id' not in params or (not LADICourse.objects.get(id=params['id'][0]).public and not request.user.is_superuser):
            return material_empty_response
    except ObjectDoesNotExist:
        return material_empty_response
    except ValueError:
        raise SuspiciousOperation("Wrong GET parameter")
    materials_path = courses_get_folder(params['id'][0])
    if not materials_path:
        return material_empty_response
    root_files = next(walk(materials_path), (None, None, []))[2]    # Add root directory
    result = [{'title': '', 'breadcrumbs': [],
               'files': [courses_pack_file(file, materials_path) for file in root_files]}]
    courses_recursive_browse(result, materials_path, MAX_DEPTH_IN_MATERIAL_SEARCH, [])
    courses_sort_material(result)
    return JsonResponse(result, safe=False)


def courses_recursive_browse(dirs_list, parent, depth, breadcrumbs):
    parent_dir = next(walk(parent), (None, None, []))
    if depth:
        for topic_title in parent_dir[1]:
            # For each subdirectory
            crumb = path.join(parent, topic_title)
            crumb = crumb.split(path.sep)
            breadcrumbs.append(str(crumb[-1]))
            dirs_list.append({'title': topic_title, 'breadcrumbs': breadcrumbs.copy(),
                              'files': courses_recursive_browse(dirs_list, path.join(parent, topic_title), depth - 1, breadcrumbs)})
            breadcrumbs.pop()
    return [courses_pack_file(file, parent) for file in parent_dir[2]]


def courses_retrieve_results(parameters):
    if parameters['keyword'] == '*':
        query_set = LADICourse.objects.all()
    else:
        query_set = LADICourse.objects.filter(course_code__exact=parameters['keyword'])
        if not query_set:
            query_set = LADICourse.objects.filter(title__contains=parameters['keyword'])
            query_set = LADICourse.objects.filter(degree_course__contains=parameters['keyword']).union(query_set)
    if 'public' in parameters['attributes']:
        return query_set.filter(public__exact=True)
    return query_set


def courses_get_folder(course_id):
    try:
        course = LADICourse.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return None
    course_dir = path.join(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users', str(course.professor_id), course.title)
    if not path.isdir(course_dir):
        return None
    return course_dir


def courses_get_file_url(parent_path, file_name):
    parent = parent_path[parent_path.find(FILEBROWSER_DIRECTORY) + len(FILEBROWSER_DIRECTORY):]
    url = str(quote("{}{}{}/{}".format(MEDIA_URL, FILEBROWSER_DIRECTORY, parent, file_name).replace('\\', '/')))
    return url.replace('%2F', '/', 1)


def courses_get_file_date(parent, filename):
    epoch = path.getmtime(path.join(parent, filename))
    return strftime('%d-%m-%Y', localtime(epoch))


def courses_get_file_size(parent, filename):
    size = path.getsize(path.join(parent, filename))
    return "{:.3f}".format(size * 9.54e-7)


def courses_pack_file(file, parent):
    return {
        'name': file,
        'url': courses_get_file_url(parent, file),
        'date': courses_get_file_date(parent, file),
        'size': courses_get_file_size(parent, file)}


def courses_sort_material(materials):
    materials.sort(key=(lambda material: len(material['breadcrumbs'])), reverse=False)


# LADILecture

def get_lectures(request):
    return db.database_search(request, LADILecture, default_attributes=mandatory_attributes(request))


def get_lectures_count(request):
    return db.database_rows_count(request, LADILecture, default_attributes=mandatory_attributes(request))


def lectures_retrieve_results(parameters):
    if parameters['keyword'] == '*':
        query_set = LADILecture.objects.all()
    else:
        query_set = LADILecture.objects.filter(title__contains=parameters['keyword'])
        query_set = LADILecture.objects.filter(text__contains=parameters['keyword']).union(query_set)
    if 'public' in parameters['attributes']:
        return query_set.filter(course__public__exact=True)
    return query_set
