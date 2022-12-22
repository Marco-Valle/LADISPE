from django.http import JsonResponse
from django.http import HttpRequest
from django.db.models.query import QuerySet

from common.database import *
from ladicontent.models import LADIForm, LADINews, LADIPicture, LADIStory, LADIGallery, LADIStaff


# Custom models attributes

class NewsAttribute(Enum):
    LADINEWS_IN_EVIDENCE = auto()


class StoryAttribute(Enum):
    LADISTORY_MATERIAL = auto()
    LADISTORY_STORY = auto()


# LADINews

def get_news(request: HttpRequest) -> JsonResponse:
    """ Get LADINews """
    query = WebQuery(request=request,
                     model=LADINews,
                     count=False,
                     model_search_func=news_retrieve_results,
                     model_attributes={'in_evidence': NewsAttribute.LADINEWS_IN_EVIDENCE}
                     )
    return query.query()


def get_news_count(request: HttpRequest) -> JsonResponse:
    """ Get LADINews rows count """
    query = WebQuery(request=request,
                     model=LADINews,
                     count=True,
                     model_search_func=news_retrieve_results,
                     model_attributes={'in_evidence': NewsAttribute.LADINEWS_IN_EVIDENCE}
                     )
    return query.query()


def news_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type == QueryType.ALL:
        query_set = LADINews.objects.all()
    else:
        query_set = LADINews.objects.filter(title__contains=query.keyword)
        query_set = LADINews.objects.filter(text__contains=query.keyword).union(query_set)
    if NewsAttribute.LADINEWS_IN_EVIDENCE in query.attributes:
        # Select the LADINews which are in evidence
        query_set = LADINews.objects.filter(in_evidence=True).intersection(query_set)
    return query_set


# LADIPicture

def get_pictures(request: HttpRequest) -> JsonResponse:
    """ Get LADIPicture """
    query = WebQuery(request=request,
                     model=LADIPicture,
                     custom_defaults={'limit': 10},
                     count=False,
                     model_search_func=pictures_retrieve_results
                     )
    return query.query()


def get_pictures_count(request: HttpRequest) -> JsonResponse:
    """ Get LADIPicture rows count """
    query = WebQuery(request=request,
                     model=LADIPicture,
                     count=True,
                     model_search_func=pictures_retrieve_results
                     )
    return query.query()


def pictures_retrieve_results(query: WebQuery) -> QuerySet:
    query_set = LADIPicture.objects.filter(gallery__description__contains=query.keyword)
    query_set = LADIPicture.objects.filter(gallery__title__startswith=query.keyword).union(query_set)
    query_set = LADIPicture.objects.filter(description__contains=query.keyword).union(query_set)
    return query_set


# LADIStory

def get_stories(request: HttpRequest) -> JsonResponse:
    """ Get LADIStory """
    query = WebQuery(request=request,
                     model=LADIStory,
                     count=False,
                     model_attributes={
                         'story_type'   :   StoryAttribute.LADISTORY_STORY,
                         'material_type':   StoryAttribute.LADISTORY_MATERIAL
                         },
                     model_search_func=stories_retrieve_results
                     )
    return query.query()


def get_stories_count(request: HttpRequest) -> JsonResponse:
    """ Get LADIStory rows count """
    query = WebQuery(request=request,
                     model=LADIStory,
                     count=True,
                     model_attributes={
                         'story_type'   :   StoryAttribute.LADISTORY_STORY,
                         'material_type':   StoryAttribute.LADISTORY_MATERIAL
                         },
                     model_search_func=stories_retrieve_results
                     )
    return query.query()


def stories_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type == QueryType.ALL:
        query_set = LADIStory.objects.all()
    else:
        query_set = LADIStory.objects.filter(title__startswith=query.keyword)
        query_set = LADIStory.objects.filter(html__contains=query.keyword).union(query_set)
        query_set = LADIStory.objects.filter(preview__contains=query.keyword).union(query_set)
        query_set = LADIStory.objects.filter(author__contains=query.keyword).union(query_set)
    if StoryAttribute.LADISTORY_STORY in query.attributes:
        query_set = LADIStory.objects.filter(type__exact=1).intersection(query_set)
    elif StoryAttribute.LADISTORY_MATERIAL in query.attributes:
        query_set = LADIStory.objects.filter(type__exact=2).intersection(query_set)
    return query_set


# LADIGallery

def get_galleries(request: HttpRequest) -> JsonResponse:
    """ Get LADIGallery """
    query = WebQuery(request=request,
                     model=LADIGallery,
                     count=False,
                     model_search_func=galleries_retrieve_results
                     )
    return query.query()


def get_galleries_count(request: HttpRequest) -> JsonResponse:
    """ Get LADIGallery rows count """
    query = WebQuery(request=request,
                     model=LADIGallery,
                     count=True,
                     model_search_func=galleries_retrieve_results
                     )
    return query.query()


def get_gallery_pictures(request: HttpRequest) -> JsonResponse:
    query = WebQuery(request=request,
                     model=LADIGallery,
                     count=False,
                     model_search_func=None
                     )
    gallery = query.get_object_from_id()
    if not gallery:
        return JsonResponse([], safe=False)
    try:
        query_set = LADIPicture.objects.filter(gallery=gallery.id)
        return JsonResponse(list(query_set.values()), safe=False)
    except AttributeError:
        return JsonResponse([], safe=False)
    


def galleries_retrieve_results(query: WebQuery) -> QuerySet:
    query_set = LADIGallery.objects.filter(description__contains=query.keyword)
    query_set = LADIGallery.objects.filter(title__startswith=query.keyword).union(query_set)
    return query_set


# LADIStaff

def get_staffs(request: HttpRequest) -> JsonResponse:
    """ Get LADIStaff """
    query = WebQuery(request=request,
                     model=LADIStaff,
                     count=False,
                     model_search_func=staffs_retrieve_results
                     )
    return query.query()


def get_staffs_count(request: HttpRequest) -> JsonResponse:
    """ Get LADIStaff rows count """
    query = WebQuery(request=request,
                     model=LADIStaff,
                     count=True,
                     model_search_func=staffs_retrieve_results
                     )
    return query.query()


def staffs_retrieve_results(query: WebQuery) -> QuerySet:
    query_set = LADIStaff.objects.filter(position__contains=query.keyword)
    return query_set


# LADIForms

def get_forms(request: HttpRequest) -> JsonResponse:
    """ Get LADIForm """
    query = WebQuery(request=request,
                     model=LADIForm,
                     count=False,
                     model_search_func=staffs_retrieve_results
                     )
    return query.query()


def get_forms_count(request: HttpRequest) -> JsonResponse:
    """ Get LADIForm rows count """
    query = WebQuery(request=request,
                     model=LADIForm,
                     count=True,
                     model_search_func=staffs_retrieve_results
                     )
    return query.query()


def forms_retrieve_results(query: WebQuery) -> QuerySet:
    if query.type == QueryType.ALL:
        query_set = LADIForm.objects.all()
    else:
        query_set = LADIForm.objects.filter(title__contains=query.keyword)
    if query.public:
        return query_set.filter(public__exact=True)
    return query_set