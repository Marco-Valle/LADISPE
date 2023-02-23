from common.database import *
from django.http import JsonResponse, HttpRequest
from filebrowser.base import FileObject

from ladicourses.coursesUtils import courseDirectory, restricted_course
from ladicourses.models import LADICourse, LADILecture

 
MATERIAL_EMPTY_RESPONSE = JsonResponse([{'title': '', 'breadcrumbs': [], 'files': []}], safe=False)


# LADICourse

def get_courses(request: HttpRequest) -> JsonResponse:
    """Get LADICourse."""
    query = WebQuery(request=request,
                     model=LADICourse,
                     count=False,
                     model_search_func=courses_retrieve_results
                     )
    return query.query()


def get_courses_count(request: HttpRequest) -> JsonResponse:
    """Get LADICourse rows count."""
    query = WebQuery(request=request,
                     model=LADICourse,
                     count=True,
                     model_search_func=courses_retrieve_results
                     )
    return query.query()


def get_courses_lectures(request: HttpRequest) -> JsonResponse:
    """Get all the LADILecture of a specific LADICourse (specified with GET parameters id)."""
    query = WebQuery(request=request, model=LADICourse, count=False)
    course = query.get_object_from_id(enforce_public=False)
    if not course or restricted_course(course=course, user=request.user):
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
    """Get the material of a specific LADICourse (specified with GET parameters id)."""
    query = WebQuery(request=request, model=LADICourse, count=False)
    course = query.get_object_from_id(enforce_public=False)
    if not course or restricted_course(course=course, user=request.user):
        return MATERIAL_EMPTY_RESPONSE
    course_foder = courseDirectory(course_title=course.title, professor_id=course.professor.id)
    if not course_foder.valid:
        return MATERIAL_EMPTY_RESPONSE
    return JsonResponse(course_foder.export_material(), safe=False)


def courses_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type in ASK_FOR_ALL:
        query_set = LADICourse.objects.all()
    else:
        query_set = LADICourse.objects.filter(course_code__exact=query.keyword)
        if not query_set:
            query_set = LADICourse.objects.filter(title__contains=query.keyword)
            query_set = LADICourse.objects.filter(degree_course__contains=query.keyword).union(query_set)
    if query.public:
        return query_set.filter(public__exact=True)
    return query_set


# LADILecture

def get_lectures(request: HttpRequest) -> JsonResponse:
    """Get LADICourse."""
    query = WebQuery(request=request,
                     model=LADILecture,
                     count=False,
                     model_search_func=lectures_retrieve_results
                     )
    return query.query()


def get_lectures_count(request: HttpRequest) -> JsonResponse:
    """Get LADICourse rows count."""
    query = WebQuery(request=request,
                     model=LADILecture,
                     count=True,
                     model_search_func=lectures_retrieve_results
                     )
    return query.query()


def lectures_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type in ASK_FOR_ALL:
        query_set = LADILecture.objects.all()
    else:
        query_set = LADILecture.objects.filter(title__contains=query.keyword)
        query_set = LADILecture.objects.filter(text__contains=query.keyword).union(query_set)
    if query.public:
        return query_set.filter(course__public__exact=True)
    return query_set
