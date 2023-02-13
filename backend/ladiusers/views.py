from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist
from django.http import JsonResponse, HttpRequest
from typing import Dict

from ladiusers.models import LADIUser
from ladicontent.models import LADIStaff
from ladicourses.models import LADICourse


def get_user(request: HttpRequest) -> JsonResponse:
    """Get a LADIUSer serialized as json from a HTTP request."""
    
    # Only user searches by ID are allowed
    parameters = get_request(request)
    if 'id' not in parameters:
        return JsonResponse([], safe=False)
    try:
        my_id = int(parameters['id'][0])
        user = search_by_id(int(parameters['id'][0]))
    except ValueError:
        return JsonResponse([], safe=False)

    # Is the user who has done the request allowed to retrieve info about this user?
    user_allowed = request.user.is_superuser or request.user == user or 'ladiusers.view_LADIUser' in request.user.get_group_permissions()
    try:
        # Is the requested user a staff member?
        LADIStaff.objects.get(user_id=my_id)
        user_visible = True
    except ObjectDoesNotExist:
        # Is the requested user a staff member of some courses?
        query_set = LADICourse.objects.filter(professor_id=my_id)
        query_set = LADICourse.objects.filter(first_assistant_id=my_id).union(query_set)
        query_set = LADICourse.objects.filter(second_assistant_id=my_id).union(query_set)
        if query_set:
            user_visible = True
        else:
            # If the user has no reason to be public, protects his and our privacy
            user_visible = False
    if user and (user_allowed or user_visible):
        # The if above is used to protect us from the user enumeration
        # Don't send the entire user, sensitive infos may be leaked (password hash, privileges...)
        result = {
            'id': my_id,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
        }
        return JsonResponse(result, safe=True)
    return JsonResponse([], safe=False)


def get_request(request: HttpRequest) -> Dict[str, str]:
    """Check for GET request and parse the parameters into a dict."""
    if request.method != 'GET':
        raise SuspiciousOperation("GET requests only")
    # Get the parameters from the request
    return request.GET.dict()


def search_by_id(my_id: int) -> LADIUser:
    """Get a LADIUser from its id."""
    try:
        return LADIUser.objects.get(id=my_id)
    except ObjectDoesNotExist:
        return None
    except ValueError:
        raise SuspiciousOperation("Wrong type")
