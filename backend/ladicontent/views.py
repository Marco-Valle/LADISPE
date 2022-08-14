from common.database import Database
from django.http import JsonResponse

from ladicontent.models import LADIForm, LADINews, LADIPicture, LADIStory, LADIGallery, LADIStaff

database_search_rules = {
    LADINews: lambda params: news_retrieve_results(params),
    LADIPicture: lambda params: pictures_retrieve_results(params),
    LADIStory: lambda params: stories_retrieve_results(params),
    LADIGallery: lambda params: galleries_retrieve_results(params),
    LADIStaff: lambda params: staffs_retrieve_results(params),
    LADIForm: lambda params: forms_retrieve_results(params),
}

db = Database(database_search_rules)
mandatory_attributes = lambda request: [] if request.user.is_superuser else ['public']  


# LADINews

def get_news(request):
    return db.database_search(request, LADINews)


def get_news_count(request):
    return db.database_rows_count(request, LADINews)


def news_retrieve_results(parameters):
    if parameters['keyword'] == '*':
        query_set = LADINews.objects.all()
    else:
        query_set = LADINews.objects.filter(title__contains=parameters['keyword'])
        query_set = LADINews.objects.filter(text__contains=parameters['keyword']).union(query_set)
    if 'in_evidence' in parameters['attributes']:
        # Select the LADINews which are in evidence
        query_set = LADINews.objects.filter(in_evidence=True).intersection(query_set)
    return query_set


# LADIPicture

def get_pictures(request):
    return db.database_search(request, LADIPicture, default_limit=10)


def get_pictures_count(request):
    return db.database_rows_count(request, LADIPicture)


def pictures_retrieve_results(parameters):
    query_set = LADIPicture.objects.filter(gallery__description__contains=parameters['keyword'])
    query_set = LADIPicture.objects.filter(gallery__title__startswith=parameters['keyword']).union(query_set)
    query_set = LADIPicture.objects.filter(description__contains=parameters['keyword']).union(query_set)
    return query_set


# LADIStory

def get_stories(request):
    return db.database_search(request, LADIStory)


def get_stories_count(request):
    return db.database_rows_count(request, LADIStory)


def stories_retrieve_results(parameters):
    if parameters['keyword'] == '*':
        query_set = LADIStory.objects.all()
    else:
        query_set = LADIStory.objects.filter(title__startswith=parameters['keyword'])
        query_set = LADIStory.objects.filter(html__contains=parameters['keyword']).union(query_set)
        query_set = LADIStory.objects.filter(preview__contains=parameters['keyword']).union(query_set)
        query_set = LADIStory.objects.filter(author__contains=parameters['keyword']).union(query_set)
    if 'story_type' in parameters['attributes']:
        query_set = LADIStory.objects.filter(type__exact=1).intersection(query_set)
    elif 'material_type' in parameters['attributes']:
        query_set = LADIStory.objects.filter(type__exact=2).intersection(query_set)
    return query_set


# LADIGallery

def get_galleries(request):
    return db.database_search(request, LADIGallery)


def get_galleries_count(request):
    return db.database_rows_count(request, LADIGallery)


def get_gallery_pictures(request):
    gallery_id = db.check_parent_id(request, LADIGallery)
    if not gallery_id:
        return JsonResponse([], safe=False)
    query_set = LADIPicture.objects.filter(gallery=gallery_id)
    return JsonResponse(list(query_set.values()), safe=False)


def galleries_retrieve_results(parameters):
    query_set = LADIGallery.objects.filter(description__contains=parameters['keyword'])
    query_set = LADIGallery.objects.filter(title__startswith=parameters['keyword']).union(query_set)
    return query_set


# LADIStaff

def get_staffs(request):
    return db.database_search(request, LADIStaff)


def get_staffs_count(request):
    return db.database_rows_count(request, LADIStaff)


def staffs_retrieve_results(parameters):
    query_set = LADIStaff.objects.filter(position__contains=parameters['keyword'])
    return query_set


# LADIForms

def get_forms(request):
    return db.database_search(request, LADIForm, default_attributes=mandatory_attributes(request))


def get_forms_count(request):
    return db.database_rows_count(request, LADIForm, default_attributes=mandatory_attributes(request))


def forms_retrieve_results(parameters):
    if parameters['keyword'] == '*':
        query_set = LADIForm.objects.all()
    else:
        query_set = LADIForm.objects.filter(title__contains=parameters['keyword'])
    if 'public' in parameters['attributes']:
        return query_set.filter(public__exact=True)
    return query_set