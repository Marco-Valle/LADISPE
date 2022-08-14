from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist, FieldError
from django.forms.models import model_to_dict
from filebrowser.base import FileObject


class Database:

    def __init__(self, database_search_rules):
        self.database_search_rules = database_search_rules

    def retrieve_results(self, model, parameters):

        if parameters['keyword'] == '*' and not parameters['attributes']:
            return model.objects.all()

        if model in self.database_search_rules:
            query_set = self.database_search_rules[model](parameters)
        else:
            query_set = model.objects.none()

        return query_set

    def database_search(self, request, model,
                        default_offset=0,
                        default_limit=100,
                        default_keyword='*',
                        default_order='timestamp',
                        default_sort='asc',
                        default_attributes=None
                        ):

        if default_attributes is None:
            # Attributes are boolean flags
            default_attributes = []

        parameters = Database.get_request(request)
        Database.set_parameter(parameters, 'attributes', default_attributes)

        if 'id' in parameters:
            try:
                # Superuser can see also not public content
                public_required = ('public' in parameters['attributes']) or not request.user.is_superuser
                return Database.search_by_id(model, int(parameters['id'][0]), public_flag_required=public_required)
            except ValueError:
                return JsonResponse([], safe=False)

        Database.set_parameter(parameters, 'offset', default_offset)
        Database.set_parameter(parameters, 'limit', default_limit)
        Database.set_parameter(parameters, 'keyword', default_keyword)
        Database.set_parameter(parameters, 'order', default_order)
        Database.set_parameter(parameters, 'sort', default_sort)

        # WHERE clause
        query_set = self.retrieve_results(model, parameters)
        # ORDERED BY
        try:
            query_set = query_set.order_by(parameters['order'])
            if parameters['sort'] == 'desc':
                query_set = query_set.reverse()
        except FieldError:
            # No ordering possible
            pass
        # SELECT fix number of elements
        data = list(query_set.values()[parameters['offset']:(parameters['offset'] + parameters['limit'])])

        if 'light' in parameters['attributes']:
            # Check if a light loading is required
            if not data:
                return JsonResponse([], safe=False)
            big_field = ['html', 'text', 'description']
            big_existent_field = []
            for field in big_field:
                if field in data[0]:
                    big_existent_field.append(field)
            for idx, result in enumerate(data):
                for field in big_existent_field:
                    try:
                        del (data[idx][field])
                    except KeyError:
                        pass
        try:
            return JsonResponse(data, safe=False)
        except TypeError:
            for idx, result in enumerate(data):
                for key, value in result.items():
                    # Check for not serializable objects and replace them with their string versions
                    if type(value) == FileObject:
                        data[idx][key] = value.path
                    elif type(value) != str and type(value) != int:
                        data[idx][key] = str(result[key])
            return JsonResponse(data, safe=False)

    def database_rows_count(self, request, model, default_attributes=None):
        if request.method != 'GET':
            raise SuspiciousOperation("GET requests only")
        if default_attributes is None:
            default_attributes = []
        # Get the parameters from the request
        parameters = dict(request.GET)
        Database.set_parameter(parameters, 'keyword', '*')
        Database.set_parameter(parameters, 'attributes', default_attributes)
        # WHERE clause
        query_set = self.retrieve_results(model, parameters)
        return JsonResponse(query_set.count(), safe=False)

    @staticmethod
    def search_by_id(model, my_id, public_flag_required=False):
        try:
            result = model.objects.get(id=my_id)
        except ObjectDoesNotExist:
            return JsonResponse([], safe=False)
        except ValueError:
            raise SuspiciousOperation("Wrong type")
        try:
            if public_flag_required and not result.public:
                return JsonResponse([], safe=False)
        except AttributeError:
            # No public flag
            pass
        try:
            return JsonResponse(model_to_dict(result), safe=True)
        except TypeError:
            result = model_to_dict(result)
            for key, value in result.items():
                # Check for not serializable objects and replace them with their string versions
                if type(value) != str and type(value) != int:
                    result[key] = str(result[key])
            return JsonResponse(result, safe=False)

    @staticmethod
    def get_parent(request, parent_model):
        parameters = Database.get_request(request)
        try:
            parent = parent_model.objects.get(id=int(parameters['id'][0]))
        except ObjectDoesNotExist:
            return None
        except ValueError:
            raise SuspiciousOperation("Wrong GET parameter")
        except KeyError:
            raise SuspiciousOperation("Wrong GET parameter")
        return parent

    @staticmethod
    def check_parent_id(request, parent_model):
        parent = Database.get_parent(request, parent_model)
        if not parent:
            return None
        return parent.id

    @staticmethod
    def get_request(request):
        if request.method != 'GET':
            raise SuspiciousOperation("GET requests only")
        # Get the parameters from the request
        return dict(request.GET)

    @staticmethod
    def set_parameter(parameters, name, default_value):
        if name in parameters:
            try:
                if name == 'attributes':
                    # Attributes are boolean flags
                    # get a list from a URL
                    parameters[name] = [str(param) for param in parameters[name][0].split(',')]
                else:
                    parameters[name] = type(default_value)(parameters[name][0])
                return
            except TypeError:
                pass
        parameters[name] = default_value
