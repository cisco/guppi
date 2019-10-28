import unittest
import plugins.AmazonService as amazon
import plugins.GoogleService as google 
import plugins.MicrosoftService as microsoft

class TestCreate(unittest.TestCase):
    def test_aws_create(self):
        service = amazon.AmazonService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
    
    def test_google_create(self):
        service = google.GoogleService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
    
    def test_microsoft_create(self):
        service = microsoft.MicrosoftService()
        beforeCreate = service.get_instances_info()
        print("before create length is: " + str(len(beforeCreate)))
        service.create_instance()
        afterCreate = service.get_instances_info()
        print("after create length is: " + str(len(afterCreate)))
        self.assertTrue(len(afterCreate) == len(beforeCreate) + 1)
