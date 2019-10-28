from abc import ABC, abstractmethod

class PluginBase(ABC):  
	@abstractmethod
	def check_setup(self):
		# Returns a boolean on whether the cloud service has been set up or not
		pass

	@abstractmethod
	def create_instance(self):
		# Creates a cloud instance
		pass
  
	@abstractmethod
	def get_instances_info(self):
		# Returns a list of instances formatted for guppi use
		pass
  
	@abstractmethod
	def terminate_instance(self, instance):
		# Deletes a cloud instance
		pass

	@abstractmethod
	def toggle_instance(self, instance):
		# Starts/stops a cloud instance
		pass

	@abstractmethod
	def reboot_instance(self, instance):
		# Restarts a cloud instance
		pass

	@abstractmethod
	def update_group(self, instance_id, group_name):
		# Updates the group of the instance
		pass

	@abstractmethod
	def get_size_list(self):
		# Returns available instance sizes
		pass

	@abstractmethod
	def get_default_size(self):
		# Returns default size value
		pass	
	
	@abstractmethod
	def get_user_and_keyname(self):
		# Returns username and keyname for ssh
		pass	
	
