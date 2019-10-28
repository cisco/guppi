import unittest
from . import test_cloud_instance_info
from . import test_cloud_create
from . import test_cloud_terminate
from . import test_slack

loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTest(loader.loadTestsFromModule(test_cloud_instance_info))
suite.addTest(loader.loadTestsFromModule(test_cloud_create))
suite.addTest(loader.loadTestsFromModule(test_cloud_terminate))
suite.addTest(loader.loadTestsFromModule(test_slack))

unittest.TextTestRunner(verbosity=3).run(suite)
