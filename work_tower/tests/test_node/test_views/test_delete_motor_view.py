from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from work_tower.models.node import NodeMotor, Node

class DeleteMotorViewTests(TestCase):
    def setUp(self):
        """Create a sample NodeMotor instance for testing"""
        self.motor = NodeMotor.objects.create(power=10.0)  
        self.url = reverse('work_tower:delete_motor')

    def test_delete_motor_with_valid_power(self):
        """Test valid deletion of a motor"""
        response = self.client.post(self.url, {
            'power': '10.0'
        })

        self.assertRedirects(response, reverse('work_tower:deleted_motor_message'))
        with self.assertRaises(NodeMotor.DoesNotExist):
            NodeMotor.objects.get(power=10.0)  

    def test_delete_motor_with_non_existent_power(self):
        """Test deletion with a non-existent motor"""
        response = self.client.post(self.url, {
            'power': '20.0'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Не знайдено двигун потужністю 20.0кВт.')

    def test_delete_motor_without_power(self):
        """Test deletion without providing power"""
        response = self.client.post(self.url, {
            'power': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введіть значення потужності двигуна.')

    def test_delete_motor_with_invalid_power(self):
        """Test deletion with invalid power input"""
        response = self.client.post(self.url, {
            'power': 'invalid_value'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Невірний ввід. Введіть числове значення потужності.')
        
        self.assertEqual(response.status_code, 200)
       
    def test_get_delete_motor_form(self):
        """Test GET request for the delete form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'work_tower/node/delete_node_motor.html')
