import unittest
import plugins.AmazonService as amazon
import plugins.GoogleService as google 
import plugins.MicrosoftService as microsoft

class TestTerminate(unittest.TestCase):
    def setUp(self):
        # set index to index to be deleted or -1 to delete the most recent instance
        self.index = -1

    def test_aws_terminate(self):
        # set service to Amazon
        service = amazon.AmazonService()
        beforeTerminate = service.get_instances_info()
        # set termIndex to the most recent instance if self.index == -1
        if(self.index < 1):
            termIndex = 0
            for index, instance in enumerate(beforeTerminate):
                # bestTime = time of most recent instance
                bestTime = beforeTerminate[termIndex]['Launch Time']
                # if launch time of current instance > best launch time set bestTime to time of current instance
                if(instance['Launch Time'] > bestTime):
                    termIndex = index
        

        service.terminate_instance(termIndex)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Amazon: nothing to terminate')
            self.assertTrue(True)        
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[termIndex]['State'] == 'shutting-down'):
            self.assertTrue(True)
        elif(afterTerminate[termIndex]['State'] == 'terminated'):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_google_terminate(self):
        # set service to Google
        service = google.GoogleService()
        beforeTerminate = service.get_instances_info()
        # set index to the most recent instance if self.index == -1
        if(self.index < 1):
            termIndex = 0
            for index, instance in enumerate(beforeTerminate):
                # bestTime = time of most recent instance
                bestTime = beforeTerminate[termIndex]['Launch Time']
                # if launch time of current instance > best launch time set bestTime to time of current instance
                if(instance['Launch Time'] > bestTime):
                    termIndex = index
        
        service.terminate_instance(termIndex)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Google: nothing to terminate')
            self.assertTrue(True)        
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[termIndex]['State'] == 'STOPPING'):
            self.assertTrue(True)
        elif(afterTerminate[termIndex]['State'] == 'TERMINATED'):
            self.assertTrue(True)

    def test_microsoft_terminate(self):
        # set service to Microsoft
        service = microsoft.MicrosoftService()
        beforeTerminate = service.get_instances_info()
        # set index to the most recent instance if self.index == -1
        if(self.index < 1):
            termIndex = 0
            for index, instance in enumerate(beforeTerminate):
                # bestTime = time of most recent instance
                bestTime = beforeTerminate[termIndex]['Launch Time']
                # if launch time of current instance > best launch time set bestTime to time of current instance
                if(instance['Launch Time'] > bestTime):
                    termIndex = index
        
        service.terminate_instance(termIndex)
        afterTerminate = service.get_instances_info()
        if(len(beforeTerminate) == 0):
            print('Microsoft: nothing to terminate')
            self.assertTrue(True)
        elif(len(afterTerminate) == len(beforeTerminate) - 1):
            self.assertTrue(True)
        elif(afterTerminate[termIndex]['State'] == 'Deleting'):
            self.assertTrue(True)