from django.shortcuts import render

from work_tower.models.substation import Substation


def substations_list_view(request):
    """
    Retrieve and display a list of all substations.
    
    Args:
        request (HttpRequest): The HTTP request object. It contains metadata about 
                               the request and is passed to the view function.

    Returns:
        HttpResponse: The rendered HTML page as a response, using the 'substation/base.html' 
                      template with the context containing all `Substation` objects.
    """
    substations = Substation.objects.all()
    context={'substations': substations}

    return render(
        request, 
        'work_tower/base_tower.html', 
        context,
        )
