import plugins

# need to pip install -U pytest
# to run: python -m pytest dbtest.py

def test_get_instance_info():
  service = plugins.AmazonService.AmazonService()
  assert isinstance(service.get_instances_info(), list)

  service = plugins.GoogleService.GoogleService()
  assert isinstance(service.get_instances_info(), list)

  service = plugins.MicrosoftService.MicrosoftService()
  assert isinstance(service.get_instances_info(), list)
