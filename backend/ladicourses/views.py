from common.database import *
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from backend.settings import MEDIA_ROOT, MEDIA_URL, FILEBROWSER_DIRECTORY, MAX_DEPTH_IN_MATERIAL_SEARCH
from os import path, walk
from urllib.parse import quote
from time import strftime, localtime
from filebrowser.base import FileObject
from typing import List, Dict, Union

from ladicourses.models import LADICourse, LADILecture

 
MATERIAL_EMPTY_RESPONSE = JsonResponse([{'title': '', 'breadcrumbs': [], 'files': []}], safe=False)


# LADICourse

def get_courses(request: HttpRequest) -> JsonResponse:
    """ Get LADICourse """
    query = WebQuery(request=request,
                     model=LADICourse,
                     count=False,
                     model_search_func=courses_retrieve_results
                     )
    return query.query()


def get_courses_count(request: HttpRequest) -> JsonResponse:
    """ Get LADICourse rows count """
    query = WebQuery(request=request,
                     model=LADICourse,
                     count=True,
                     model_search_func=courses_retrieve_results
                     )
    return query.query()


def get_courses_lectures(request: HttpRequest) -> JsonResponse:
    query = WebQuery(request=request, model=LADICourse, count=False)
    course = query.get_object_from_id(enforce_public=False)
    if not course:
        return JsonResponse([], safe=False)
    if not course.public and not request.user.is_superuser:
        allowed_users = {course.professor, course.first_assistant, course.second_assistant}
        if request.user not in allowed_users:
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


def get_courses_materials(request: HttpRequest) -> JsonResponse:
    query = WebQuery(request=request, model=LADICourse, count=False)
    course = query.get_object_from_id()
    materials_path = courses_get_folder(course.id)
    if not materials_path:
        return MATERIAL_EMPTY_RESPONSE
    root_files = next(walk(materials_path), (None, None, []))[2]    # Add root directory
    result = [{'title': '', 'breadcrumbs': [],
               'files': [courses_pack_file(file, materials_path) for file in root_files]}]
    courses_recursive_browse(result, materials_path, MAX_DEPTH_IN_MATERIAL_SEARCH, [])
    courses_sort_material(result)
    return JsonResponse(result, safe=False)


def courses_recursive_browse(dirs_list: List[Dict[str, Union[str, List[str], List[Dict[str, str]]]]],
                             parent: str,
                             depth: int,
                             breadcrumbs: List[str]
                             ) -> List[Dict[str, str]]:
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


def courses_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type == QueryType.ALL:
        query_set = LADICourse.objects.all()
    else:
        query_set = LADICourse.objects.filter(course_code__exact=query.keyword)
        if not query_set:
            query_set = LADICourse.objects.filter(title__contains=query.keyword)
            query_set = LADICourse.objects.filter(degree_course__contains=query.keyword).union(query_set)
    if query.public:
        return query_set.filter(public__exact=True)
    return query_set


def courses_get_folder(course_id: int) -> Optional[str]:
    try:
        course = LADICourse.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return None
    course_dir = path.join(MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'Users', str(course.professor_id), course.title)
    if not path.isdir(course_dir):
        return None
    return course_dir


def courses_get_file_url(parent_path: str, file_name: str) -> str:
    parent = parent_path[parent_path.find(FILEBROWSER_DIRECTORY) + len(FILEBROWSER_DIRECTORY):]
    url = str(quote("{}{}{}/{}".format(MEDIA_URL, FILEBROWSER_DIRECTORY, parent, file_name).replace('\\', '/')))
    return url.replace('%2F', '/', 1)


def courses_get_file_date(parent: str, filename: str) -> str:
    epoch = path.getmtime(path.join(parent, filename))
    return strftime('%d-%m-%Y', localtime(epoch))


def courses_get_file_size(parent: str, filename: str) -> str:
    size = path.getsize(path.join(parent, filename))
    return "{:.3f}".format(size * 9.54e-7)


def courses_pack_file(file: str, parent: str) -> List[Dict[str, str]]:
    return {
        'name': file,
        'url': courses_get_file_url(parent, file),
        'date': courses_get_file_date(parent, file),
        'size': courses_get_file_size(parent, file)}


def courses_sort_material(materials: List[Dict[str, Union[str, List[str], List[Dict[str, str]]]]]
                          ) -> List[Dict[str, Union[str, List[str], List[Dict[str, str]]]]]:
    materials.sort(key=(lambda material: len(material['breadcrumbs'])), reverse=False)


# LADILecture

def get_lectures(request: HttpRequest) -> JsonResponse:
    """ Get LADICourse """
    query = WebQuery(request=request,
                     model=LADILecture,
                     count=False,
                     model_search_func=lectures_retrieve_results
                     )
    return query.query()


def get_lectures_count(request: HttpRequest) -> JsonResponse:
    """ Get LADICourse rows count """
    query = WebQuery(request=request,
                     model=LADILecture,
                     count=True,
                     model_search_func=lectures_retrieve_results
                     )
    return query.query()


def lectures_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type == QueryType.ALL:
        query_set = LADILecture.objects.all()
    else:
        query_set = LADILecture.objects.filter(title__contains=query.keyword)
        query_set = LADILecture.objects.filter(text__contains=query.keyword).union(query_set)
    if query.public:
        return query_set.filter(course__public__exact=True)
    return query_set
