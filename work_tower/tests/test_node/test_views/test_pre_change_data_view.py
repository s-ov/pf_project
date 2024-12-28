from django.test import TestCase
from django.urls import reverse

class PreChangeDataViewTest(TestCase):
    def test_pre_change_data_view(self):
        """
        Test that the view renders the 'pre_change_data.html' template.
        """
        
        url = reverse('work_tower:pre_change_data')  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'work_tower/node/pre_change_data.html')
