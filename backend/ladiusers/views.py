from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist
from django.http import JsonResponse, HttpRequest
from typing import Dict

from common.database import *
from ladiusers.models import LADIUser
from ladicontent.models import LADIStaff
from ladicourses.models import LADICourse


def get_user(request: HttpRequest) -> JsonResponse:
    """Get a LADIUSer serialized as json from a HTTP request."""
    
    query = WebQuery(request=request, model=LADIUser)
    if query.type != QueryType.BY_ID:
        # Only user searches by ID are allowed
        return JsonResponse([], safe=False)
    
    user = query.get_object_from_id(enforce_public=False)
    if not user:
        return JsonResponse([], safe=False)
    
    if not(request.user.is_superuser or request.user == user or 'ladiusers.view_LADIUser' in request.user.get_group_permissions()):
        try:
            # Is the requested user a staff member?
            LADIStaff.objects.get(user_id=query.obj_id)
            restricted_user = False
        except ObjectDoesNotExist:
            # Is the requested user a staff member of some courses?
            query_set = LADICourse.objects.filter(professor_id=query.obj_id, private_email=False)
            query_set = LADICourse.objects.filter(first_assistant_id=query.obj_id, private_email=False).union(query_set)
            query_set = LADICourse.objects.filter(second_assistant_id=query.obj_id, private_email=False).union(query_set)
            restricted_user = False if query_set and query_set.count() else True

    if restricted_user:
        return JsonResponse([], safe=False)

    # Don't send the entire user, sensitive infos may be leaked (password hash, privileges...)
    result = {
        'id': query.obj_id,
        'name': user.name,
        'surname': user.surname,
        'email': user.email,
    }
    return JsonResponse(result, safe=True)
