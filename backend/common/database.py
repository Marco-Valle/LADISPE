from __future__ import annotations
import builtins
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation, ObjectDoesNotExist, FieldError
from django.forms.models import model_to_dict
from django.db.models.query import QuerySet
from django.db.models import Model
from django.http import HttpRequest
from filebrowser.base import FileObject
from typing import Dict, Callable, List, Set, Any, Union, Optional
from enum import Enum, auto
from dataclasses import field, dataclass


class QueryType(Enum):
    ALL = auto()
    BY_ID = auto()
    BY_KEYWORD = auto()
    COUNT_ALL = auto()
    COUNT_BY_KEYWORD = auto()
    INVALID = auto()
    
    
class QueryAttribute(Enum):
    LIGHT = auto()
    PUBLIC = auto()


class SortType(Enum):
    ASCENDING = auto()
    DESCENDING = auto()
    

class WebQueryTypeError(TypeError):
    """WebQuery type error

    Attributes:
        wrong_type          --  the type of WebQuery
        missing_property    --  the property that cannot be accessed
    """
    
    missing_property    :   str
    wrong_type          :   QueryType
    
    
    def __init__(self, wrong_type: QueryType, missing_property: str) -> None:
        super().__init__()
        self.wrong_type = wrong_type
        self.missing_property = missing_property
        
    
    def __str__(self) -> str:
        return f"WebQuery of type {self.wrong_type} doesn't have property {self.missing_property}"


@dataclass
class WebQueryOptions:
    """WebQuery class options."""
    
    limit               :   int                                         =   100
    obj_id              :   int                                         =   -1
    offset              :   int                                         =   0
    privileged          :   bool                                        =   False
    keyword             :   str                                         =   ''
    order_by            :   str                                         =   'timestamp'
    sort                :   SortType                                    =   SortType.ASCENDING
    attributes          :   Set[Union[QueryAttribute, Any]]             =   field(default_factory=set)
    

class WebQuery:
    """WebQuery class can be use to query the dbms from an HTTP request and return a json or a db obj."""
    
    
    model               :   Model
    options             :   WebQueryOptions  
    type                :   QueryType                                       =   QueryType.INVALID                        
    model_search_func   :   Optional[Callable[[WebQuery], QuerySet[Any]]]   =   None
    
    
    def __init__(self,
                 request            :   HttpRequest,
                 model              :   Model,
                 count              :   bool                                        =   False,
                 model_attributes   :   Dict[str, Any]                              =   {},
                 model_search_func  :   Optional[Callable[[WebQuery], QuerySet[Any]]]    =   None,
                 custom_defaults    :   Optional[Dict[str, Union[int, str, bool]]]  =   None
                 ) -> None:
        """Initializer of the WebQuery class."""
        
        # Set attributes without default value
        self.options = WebQueryOptions()
        self.model = model
        if not model:
            self.type = QueryType.INVALID
            return
        
        if model_search_func:
            self.model_search_func = model_search_func
        
        req_params = WebQuery._parse_GET(request=request)
        if request.user.is_superuser:
            self.options.privileged = True
        
        # Set custom default values
        defaults_allowed_types = {int, str, bool}
        if not custom_defaults:
            custom_defaults = {}
        for key, value in custom_defaults.items():
            if key == 'privileged':
                continue
            if key in self.options.__annotations__ and self.options.__annotations__[key] in defaults_allowed_types:
                setattr(self.options, key, self.options.__annotations__[key](value))
        
        # Set query type
        if req_params.get('id'):
            self.type = QueryType.BY_ID
        elif not req_params.get('keyword') or req_params.get('keyword') == '*':
            self.type = QueryType.ALL if not count else QueryType.COUNT_ALL
        else:
            self.type = QueryType.BY_KEYWORD if not count else QueryType.COUNT_BY_KEYWORD
        
        # Set attributes and parameters
        if req_params.get('attributes'):
            self._set_attributes(attributes_str=str(req_params.get('attributes')), model_attributes=model_attributes)
        self._set_parameters(req_params) 
    
    
    @property
    def attributes(self) -> Set[Union[QueryAttribute, Any]]:
        if self.type == QueryType.INVALID:
            raise WebQueryTypeError(wrong_type=self.type, missing_property='attributes')
        return self.options.attributes
    
    
    @property
    def keyword(self) -> str:
        query_by_keyword_types = {QueryType.COUNT_BY_KEYWORD, QueryType.BY_KEYWORD}
        if self.type not in query_by_keyword_types:
            raise WebQueryTypeError(wrong_type=self.type, missing_property='keyword')
        return self.options.keyword
  
      
    @property 
    def light(self) -> bool:
        if self.type == QueryType.INVALID:
            raise WebQueryTypeError(wrong_type=self.type, missing_property='light')
        return QueryAttribute.LIGHT in self.options.attributes
    
    
    @property
    def obj_id(self) -> int:
        if self.type != QueryType.BY_ID:
            raise WebQueryTypeError(wrong_type=self.type, missing_property='obj_id')
        return self.options.obj_id
    
        
    @property 
    def public(self) -> bool:
        if self.type == QueryType.INVALID:
            raise WebQueryTypeError(wrong_type=self.type, missing_property='public')
        return QueryAttribute.PUBLIC in self.options.attributes
        
        
    def query(self) -> JsonResponse:
        """Query the dbms and return a json."""
        
        if self.type == QueryType.INVALID:
            return JsonResponse([], safe=False)
        elif self.type == QueryType.BY_ID:
            obj = self.get_object_from_id()
            return self._json_from_object(obj=obj)
        
        query_set = self._get_queryset()
        if self.type in {QueryType.COUNT_ALL, QueryType.COUNT_BY_KEYWORD}:
            return JsonResponse(data=query_set.count, safe=False)
        
        return self._json_from_queryset(query_set=query_set)
    
    
    def get_object_from_id(self, enforce_public: bool = True) -> Any:
        """Get a db object from its id."""
        
        if self.type != QueryType.BY_ID:
            return None
        
        try:
            obj = self.model.objects.get(id=self.obj_id)
        except ObjectDoesNotExist:
            return None
        except ValueError:
            raise SuspiciousOperation("Wrong type")
        
        try:
            if enforce_public and self.public and not obj.public:
                return None
        except AttributeError:
            # No public flag
            pass
        
        return obj
    
    
    def _get_queryset(self) -> QuerySet[Any]:
        """Get a QuerySet."""
        
        if self.type not in {QueryType.ALL, QueryType.BY_KEYWORD}:
            return self.model.objects.none()
        
        if self.type == QueryType.ALL and not self.public:
            query_set = self.model.objects.all()
        elif self.model_search_func:
            query_set = self.model_search_func(self)
        else:
            return self.model.objects.none()
            
        if not query_set.count:
            return self.model.objects.none()
        
        # ORDERED BY
        try:
            query_set = query_set.order_by(self.options.order_by)
            if self.options.sort == SortType.DESCENDING:
                query_set = query_set.reverse()
        except FieldError:
            # No ordering possible
            pass
        
        return query_set
    
        
    def _set_attributes(self, attributes_str: str, model_attributes: Dict[str, Any]) -> None:
        """Used by __init__ to import the attributes."""
        
        attributes = [str(param).strip() for param in attributes_str.split(',')]
        if 'light' in attributes:
            self.options.attributes.add(QueryAttribute.LIGHT)
        if 'public' in attributes or not self.options.privileged:
            self.options.attributes.add(QueryAttribute.PUBLIC)
        
        for key, value in model_attributes.items():
            if key in attributes:
                self.options.attributes.add(value)
            
            
    def _set_parameters(self, req_params: Dict[str, Union[str, List[str]]]) -> None:
        """Set the query options from the request parameters."""
        
        id_func: Callable[[str], Any] = lambda value: int(value) if self.type == QueryType.BY_ID else -1
        keyword_func: Callable[[str], Any] = lambda value: value if self.type in {QueryType.ALL, QueryType.BY_KEYWORD} else ''
        sort_func: Callable[[str], Any] = lambda value: SortType.DESCENDING if value  == 'desc'  else SortType.ASCENDING
        custom_options = {'obj_id': id_func, 'keyword': keyword_func, 'sort': sort_func}
        trusted_types = {'int', 'str'}
        
        try:       
            for key, param_type in self.options.__annotations__.items():
                value = req_params.get(key) if key != 'obj_id' else req_params.get('id')
                if value is None:
                    continue
                if type(value) == List[str]:
                    value = value[0] if len(value) > 0 else ''
                if key in custom_options:
                    setattr(self.options, key, custom_options[key](value))
                elif param_type in trusted_types:
                    setattr(self.options, key, getattr(builtins, param_type)(value))
                
        except KeyError:
            self.type = QueryType.INVALID
            return 
        
        except TypeError:
            self.type = QueryType.INVALID
            return 
                
        except ValueError:
            self.type = QueryType.INVALID
            return
        
        
    def _json_from_queryset(self, query_set: QuerySet[Any]) -> JsonResponse:
        """Get a json from a QuerySet."""
        
        if not query_set.count():
            return JsonResponse(data=[], safe=False)
        
        # SELECT fix number of elements
        data = list(query_set.values()[self.options.offset:(self.options.offset + self.options.limit)])
        
        if self.light:
            WebQuery._lighten_data_list(data_list=data)
        
        try:
            return JsonResponse(data=data, safe=False)
        except TypeError:
            for idx, obj in enumerate(data):
                for key, value in obj.items():
                    # Check for not serializable objects and replace them with their string versions
                    if type(value) == FileObject:
                        data[idx][key] = value.path
                    elif type(value) != str and type(value) != int:
                        data[idx][key] = str(obj.get(key))
            return JsonResponse(data=data, safe=False)
        
        
    def _json_from_object(self, obj: Any) -> JsonResponse:
        """Get a json from a db object."""
        
        if self.type != QueryType.BY_ID or not obj:
            return JsonResponse(data=[], safe=False)
        
        try:
            return JsonResponse(data=model_to_dict(obj), safe=True)
        except TypeError:
            obj = model_to_dict(obj)
            for key, value in obj.items():
                # Check for not serializable objects and replace them with their string versions
                if type(value) != str and type(value) != int:
                    obj[key] = str(obj[key])
            return JsonResponse(data=obj, safe=True)
     
     
    @staticmethod
    def _lighten_data_list(data_list: List[Dict[str, Any]]) -> None:
        """Remove some large fields from a dict containing the db objects attributes."""
        for idx, item in enumerate(data_list):
            big_fields = {'html', 'text', 'description'}.intersection(item.keys())
            for key in big_fields:
                del(data_list[idx][key])
        
        
    @staticmethod
    def _parse_GET(request: HttpRequest) -> Dict[str, Union[str, List[str]]]:
        """Check that the GET request and return a dict."""
        
        if request.method != 'GET':
            raise SuspiciousOperation("GET requests only")
        
        return request.GET.dict()
                
