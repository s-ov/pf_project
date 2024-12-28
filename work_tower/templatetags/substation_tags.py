from django import template
from work_tower.models.substation import Substation

register = template.Library()


@register.inclusion_tag('work_tower/substations_list.html')
def show_substations():
    """
        Fetch all Substation instances

    Returns:
        Collection of Substation instances
    """
    return {'substations': Substation.objects.all(),}
