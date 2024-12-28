from django.test import SimpleTestCase
from django.urls import reverse, resolve
from work_tower.views.substation import substations_list_view

class SubstationURLTests(SimpleTestCase):
    def test_substations_url_resolves(self):
        """
        Test that the URL for the substations list view resolves correctly.
        """
        url = reverse('work_tower:substations')  
        self.assertEqual(resolve(url).func, substations_list_view)
