from django.test import TestCase
from django.urls import reverse
from django.http import Http404

from work_tower.models.substation import Substation
from work_tower.models.mcc import MotorControlCenter as MCC
from work_tower.models.node import Node

class URLResolutionTests(TestCase):

    def setUp(self):
        """Create test data for URL resolution tests."""
        self.substation = Substation.objects.create(slug='test-substation', title='Test Substation')
        self.mcc = MCC.objects.create(slug='test-mcc', title='Test MCC', substation=self.substation)
        
        self.node1 = Node.objects.create(name='Node 1', mcc=self.mcc, index='node_1')
        self.node2 = Node.objects.create(name='Node 2', mcc=self.mcc, index='node_2')

    def test_substation_mccs_url_resolution(self):
        """Test that the URL for the substation MCCs view resolves correctly."""
        url = reverse('work_tower:substation_mccs', kwargs={'substation_slug': self.substation.slug})
        self.assertEqual(url, f'/work_tower/substation/{self.substation.slug}/')

    def test_mcc_nodes_url_resolution(self):
        """Test that the URL for the MCC nodes view resolves correctly."""
        url = reverse('work_tower:mcc_detail', kwargs={'mcc_slug': self.mcc.slug})
        self.assertEqual(url, f'/work_tower/mcc/{self.mcc.slug}/')
