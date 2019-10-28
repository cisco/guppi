from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, Markdown
import glob
import re
import src.plugins as plugins
import sys
import paramiko

import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
import src.user_interfaces as user_interfaces

selected_instance = ""
accordion =""

# Setting default service
service = ""

@magics_class
class GuppiMagic(Magics):

	# initializes file from interfaces and services folders
	filenames = glob.glob('src/plugins/*')
	python_files = []

	#title display
	icon_file = open("src/icons/guppi-small.png", "rb")
	image = icon_file.read()
	logo = widgets.Image(value=image,format='png',width = 100,height = 100)
	title = widgets.HTML("<h2>Project GUPPI</h2>")
	title_box = widgets.Box([title])
	display(title_box)
	display(logo)

	print("For useage: use %guppi help")
	f = None
	python_file = None
	for f in filenames:
		python_file = f

		python_file = python_file[12:]
		if python_file == 'pluginbase.py':
			continue
		if python_file == '__pycache__':
			continue
		if python_file == '__init__.py':
			continue
		pattern = re.compile('.pyc')
		if pattern.search(python_file):
			continue
		python_file = re.sub('.py', '', python_file)	
		python_files.append(python_file)

	cloud_list = []
	cloud_index = 0
	file_name = None
	module_name = None
	mod_class = None
	for file_name in python_files:
		module_name = getattr(plugins, file_name)
		mod_class = getattr(module_name, file_name)
		service = mod_class()
		cloud_list.append(service)
		print("loading plugin: "+ file_name)
	print("plugins loaded")

	@line_magic
	@magic_arguments.magic_arguments()
	@magic_arguments.argument('arguments', nargs='*')
	def guppi(self, line=''):
		args = magic_arguments.parse_argstring(self.guppi, line)

		if(len(args.arguments) > 0):
			# switch service
			if(args.arguments[0] == 'switch'):
				if(len(args.arguments) < 3 and len(args.arguments) > 1):
					i = 0
					for file_name in self.python_files:
						if(args.arguments[1] == file_name):
							self.cloud_index = i
							print('set cloud interactions to '+file_name)
						i = i+1
				else:
					print("Not a valid command, type guppi switch followed by the service provider, valid services:")
					for file_name in self.python_files:
						print(file_name)

			# cloud services
			elif(args.arguments[0] == 'cloud'):
				i = 1
				
				# set serviceStr to cloud service
				if len(args.arguments) > 1:
					serviceStr = args.arguments[i]
					i += 1
				else:
					print("Please enter a cloud service, the available services are:")
					for file_name in self.python_files:
						print(" -- "+file_name[0:-7].lower())
					print("or choose multicloud to view all services")
					return 

				
				# ssh service
				if len(args.arguments) > 2:
					if args.arguments[i] == 'ssh':
						i += 1
						verbose = False
						if len(args.arguments) > 3:
							
							# cloud ssh view mode
							if args.arguments[i] == 'view':
								if serviceStr.casefold() == 'multicloud':
									user_interfaces.SshInterface.render_ssh_interface(self.cloud_list, -1, verbose)
								else:
									index = 0
									for i, cloudService in enumerate(self.cloud_list):
										if cloudService.name.casefold() == serviceStr.casefold():
											index = i
									user_interfaces.SshInterface.render_ssh_interface(self.cloud_list, index, verbose)
								return
							
							# verbose flag for ssh non-view
							if args.arguments[i] == 'v':
								i += 1
								verbose = True
							
							# check for group name
							if len(args.arguments) < i + 1:
								print('Please provide group name')
								print('Run %guppi help for the list of commands')
							else:
								#set group_name
								group_name = args.arguments[i]
								i += 1
								# if multicloud
								if serviceStr.casefold() == 'multicloud'.casefold():
									noInstancesFlag = True
									for cloudService in self.cloud_list:
										cloudName = cloudService.name
										instances = cloudService.get_instances_info()
										sshInstances = []			
										for instance in instances:
											if instance['Group Name'] == group_name:
												if instance['State'] == 'running':
													sshInstances.append(instance)
										commands = ' '.join(args.arguments[i:])
										if len(sshInstances) > 0:
											noInstancesFlag = False
											print(cloudName.upper())
											cloudService.ssh(sshInstances, commands, verbose)
									
									if noInstancesFlag == True:
										print('No instances in group \'' + group_name + '\'')
								else:
									for cloudService in self.cloud_list:
										if cloudService.name.casefold() == serviceStr.casefold():
											instances = cloudService.get_instances_info()
						
									sshInstances = []			
									for instance in instances:
										if instance['Group Name'] == group_name:
											if instance['State'] == 'running':
												sshInstances.append(instance)
									commands = ' '.join(args.arguments[i:])
									
									if len(sshInstances) == 0:
										print('No instances in group \'' + group_name + '\'')
									else:
										for cloudService in self.cloud_list:
											if cloudService.name.casefold() == serviceStr.casefold():
												cloudService.ssh(sshInstances, commands, verbose)
						else:
							print("Please enter an ssh mode")
							print('Run %guppi help for the list of commands')

					
					# create instance
					elif(args.arguments[i] == 'create'):
						index = 0
						for i, cloudService in enumerate(self.cloud_list):
							if cloudService.name.casefold() == serviceStr.casefold():
								index = i
						user_interfaces.CreateInterface.render_create_interface(self.cloud_list, index)
					
					# view interface
					elif(args.arguments[i] == 'view'):
						if(args.arguments[i-1] == "multicloud"):
							user_interfaces.CloudInterface.render_cloud_interface(self.cloud_list,-1)
						else:
							index = 0
							for i, cloudService in enumerate(self.cloud_list):
								if cloudService.name.casefold() == serviceStr.casefold():
									index = i
							user_interfaces.CloudInterface.render_cloud_interface(self.cloud_list, index)
					
					else:
						print(args.arguments[i] +" is not a cloud command, for usage, use %guppi help")
				else:
					print("Please enter a cloud command to use. eg: view, ssh, create")
					print('Run %guppi help for the list of commands')

			#slack service
			elif(args.arguments[0] == 'slack'):
				if(len(args.arguments)>1):
					if(args.arguments[1] == 'view'):
						if(len(args.arguments)< 3):
							# user_interfaces.SlackInterface.render_slack_interface()
							print("")
						else:
							print(args.arguments[2] +" is not a slack command, for usage, use %guppi help")
					elif(args.arguments[1] == 'send'):
						if(len(args.arguments)< 2):
							print("Please enter a channel name: %guppi slack send <channel_name> <\"MESSAGE\">")
						else:
							if(len(args.arguments)< 4):
								print("Please enter a message: %guppi slack send <channel_name> <\"MESSAGE\">")
								print("Note: message must be in quotes")
							elif(len(args.arguments)> 4):
								print("Your message must be in quotes")
							else:
								# user_interfaces.SlackInterface.send_message(args.arguments[2],args.arguments[3])
								print("")
					else:
						print(args.arguments[1] +" is not a slack command, for usage, use %guppi help")
				else:
					print("For Slack usage, use %guppi help ")

			# github service
			elif(args.arguments[0] == 'github'):
				if(len(args.arguments) < 2):
					user_interfaces.GitHubInterface.display_notifications(5)
				else:
					try:
						num = int(args.arguments[1])
					except ValueError:
						print("Number of notifications must be an integer")
					else:
						user_interfaces.GitHubInterface.display_notifications(num+1)
			elif(args.arguments[0] == 'help'):
				fn = "guppihelp.md"
				help_markdown = open(fn, 'r').read()
				display(Markdown(help_markdown))
			else:
				print(args.arguments[0] + " is not a guppi command, for usage, use %guppi help")
					
		else:
			print("For usage, use the %guppi help command")


#===================================================#
#-----------ipython-Magic-Registering---------------#
#===================================================#

def load_ipython_extension(ipython):
	"""This function is called when the extension is
	loaded. It accepts an IPython InteractiveShell
	instance. We can register the magic with the
	`register_magic_function` method of the shell
	instance."""
	ipython.register_magics(GuppiMagic)
