import unittest
import plugins

class TestGetInstanceInfo(unittest.TestCase):
    def setUp(self):
        self.test = "test"
    
    def test_aws(self):
        service = plugins.AmazonService.AmazonService()
        assert isinstance(service.get_instances_info(), list)
    def test_google(self):
        service = plugins.GoogleService.GoogleService()
        assert isinstance(service.get_instances_info(), list)
    def test_microsoft(self):
        service = plugins.MicrosoftService.MicrosoftService()
        assert isinstance(service.get_instances_info(), list)