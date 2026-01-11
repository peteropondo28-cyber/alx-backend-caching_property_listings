from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = get_all_properties()
    
    # Convert queryset to list of dicts
    property_data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": str(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat()
        } for p in properties
    ]
    
    # Return as a dictionary inside JsonResponse
    return JsonResponse({"properties": property_data})
