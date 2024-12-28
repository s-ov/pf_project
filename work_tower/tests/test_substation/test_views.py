from django.test import TestCase, Client
from django.urls import reverse
from work_tower.models.substation import Substation

class SubstationsListViewTests(TestCase):
    def setUp(self):
        """ Set up the client and some initial data for testing """
        self.client = Client()
        self.response = self.client.get(reverse('work_tower:substations')) 
        self.substation1 = Substation.objects.create(title='Substation 1', slug='substation-1')
        self.substation2 = Substation.objects.create(title='Substation 2', slug='substation-2')

    def test_substations_list_view_status_code(self):
        """ Test the status code of the response """
        self.assertEqual(self.response.status_code, 200)

    def test_substations_list_view_template(self):
        """ Test the template used in the response """
        self.assertTemplateUsed(self.response, 'work_tower/base_tower.html')

    def test_substations_list_view_context(self):
        """ Test the context of the response """
        self.assertIn('substations', self.response.context)
        self.assertEqual(list(self.response.context['substations']), [self.substation1, self.substation2])
