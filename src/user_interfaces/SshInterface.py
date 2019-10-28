from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink, clear_output
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider


import src.plugins as plugins
import paramiko
import warnings
import threading
import io

warnings.filterwarnings(action='ignore',module='.*paramiko.*')

# def ssh(instances, commands, verbose):
# 	# clear_output()
# 	print("Running, please wait...")
	
# 	# threadOutputList contains list of all shell outputs
# 	threadOutputList = []
	
# 	# threadErrorList contains list of all shell errors
# 	threadErrorList = []
	
# 	# sshThread gets called by each thread
# 	def sshThread(commands, instanceId):
# 		# set the dns for each instance
# 		Dns = ''
# 		for vm in instances:
# 			if(instanceId == vm['Instance Id'] or instanceId == vm['Name']):
# 				Dns = vm['Dns']
		
# 		# ssh in and run commands
# 		ssh = paramiko.SSHClient()
# 		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 		user_and_key = service.get_user_and_keyname()

# 		ssh.connect(Dns,
# 					username=user_and_key[0],
# 					key_filename=user_and_key[1])
	
# 		stdin, stdout, stderr = ssh.exec_command(commands)
# 		stdin.flush()
		
# 		# create list of all lines of output
# 		outputList = []
# 		outputList.append("=======================================================")
# 		outputList.append(instanceId)
# 		outputList.append("=======================================================")
# 		for line in stdout.read().splitlines():
# 			outputList.append(line)
# 		# create list of all lines of errors
# 		errorList = []
# 		errorList.append("=======================================================")
# 		errorList.append(instanceId)
# 		errorList.append("=======================================================")
# 		errorOutput = stderr.read().splitlines()
# 		numOfCommands = len(commands.split(" "))
		
# 		# if no errors append "successfully run" to output and error lists
# 		if len(errorOutput) == 0:
# 			if numOfCommands == 1:
# 				errorList.append("Successfully ran 1 command\n")
# 				outputList.append("Successfully ran 1 command\n")
# 			else:
# 				errorList.append("Successfully ran " + str(numOfCommands) + " commands\n")
# 				outputList.append("Successfully ran " + str(numOfCommands) + " commands\n")
		
# 		# append errors to the errorList
# 		for line in errorOutput:
# 			errorList.append(line)

# 		# append errorList to threadErrors
# 		threadErrorList.append(errorList)

# 		# append outputList to the threadOutputs
# 		threadOutputList.append(outputList)
		
# 		# disconnect from instance
# 		ssh.close()
	
# 	# theadList will contain a thread for each instance
# 	threadList = []
	
# 	# for each checked instance create a thread
# 	for instance in instances:
# 			thread = threading.Thread(target=sshThread, args=(commands, instance['Instance Id'])) 
# 			thread.start()
# 			threadList.append(thread)

# 	# wait for each thread to finish
# 	for thread in threadList:
# 		thread.join()
	
# 	# if verbose flag is used print output from each instance shell
# 	if verbose:		
# 		for data in threadOutputList:
# 			for output_line in data:
# 				print(output_line)
# 	# else just print errors from each instance shell
# 	else:
# 		for errors in threadErrorList:
# 			for output_line in errors:
# 				print(output_line)


#===================================================#
#--------------SSH-Interface-Function---------------#
#===================================================#
def render_ssh_interface(cloud_list, cloud_index, verbose):
	title = widgets.HTML("<h4>SSH into instances </h4>")
	display(title)
	service = cloud_list[cloud_index]
	instances = []
	

	#multicloud adds all instances to instance list and appends index
	if(cloud_index < 0):
		for cloud in cloud_list:
			inst_info = cloud.get_instances_info()
			ind = 0
			for info in inst_info:
				info['index'] = ind
				instances.append(info)
				ind+=1
	else:
		instances = cloud_list[cloud_index].get_instances_info()

	group_list = []

	for instance in instances:
		group_name = instance['Group Name']
		if group_name not in group_list and group_name != '':
			group_list.append(group_name)

	group_list.sort(key=str.lower)
	tab_arr = []
	layout_arr = render_group(instances,'All Instances', verbose, service,cloud_list)
	tab_child = widgets.VBox(layout_arr)
	tab_arr.append(tab_child)

	#multicloud addding separate cloud tabs
	if cloud_index < 0:
		c_index = 0
		start_index = 0
		for cloud in cloud_list:
			service_length = len(cloud.get_instances_info())
			cloud_instances = instances[start_index:start_index + service_length]
			cloud_layout_arr = render_group(cloud_instances,"service_group",verbose, cloud_list[c_index], cloud_list)
			child = widgets.VBox(cloud_layout_arr)
			tab_arr.append(child)
			start_index += service_length
			c_index += 1

	tab = widgets.Tab()
	for group_name in group_list:
		layout_arr = render_group(instances,group_name, verbose, service, cloud_list)
		tab_child = widgets.VBox(layout_arr)
		tab_arr.append(tab_child)
	
	tab.children = tab_arr
	tab.set_title(0,'All Instances')
	# set titles for tab
	#setting tab titles in multicloud
	offset = 1

	if cloud_index < 0:
		for cloud in cloud_list:
			tab.set_title(offset,cloud.name + " Instances")
			offset+=1

	# set titles for tab
	for i in range(len(group_list)):
		tab.set_title(i+offset, group_list[i])

	display(tab)
	

def render_group(instances, group_name, verbose, service, cloud_list):
	group_layout_arr = []

	# instances = cloud_list[0].get_instances_info()
	box_list = []
	instance_boxes = []

	#creates the checkboxes
	for vm in instances:
		if vm['State'] == 'running' and (vm['Group Name'] == group_name or group_name == 'All Instances' or group_name == 'service_group'):
			if(vm['Name'] == ''):	
				cb = widgets.Checkbox(
					value=True,
					description=vm['Instance Id'],
					disabled=False,
				)
			else:
				cb = widgets.Checkbox(
					value=True,
					description=vm['Name'],
					disabled=False
				)
			instance_boxes.append(cb)
			box_list.append(cb)
	
	select_button = widgets.Button(
			description='Select All',
			disabled=False,
			tooltip='',
			icon='check',

		)	
	submit_button = widgets.Button(
		description='Run Commands',
		disabled=False,
		tooltip='',
		layout=Layout(width='30%', height='40px')
	)
	
	submit_button_v = widgets.Button(
		description='Run Commands Verbose',
		disabled=False,
		tooltip='',
		layout=Layout(width='30%', height='40px')
	)
	button_box= widgets.HBox([submit_button,submit_button_v])
	if(len(box_list) == 0):
		if(group_name != "All Instances"):
			group_layout_arr.append(widgets.HTML(value="There are no running instances in " + group_name))
		else:
			group_layout_arr.append(widgets.HTML(value="There are no running instances"))

	else:
		# display(select_button)
		group_layout_arr.append(select_button)

		box_array = []

		for i in range(0, len(instance_boxes), 3):
			box_array.append(instance_boxes[i:i+3])
		
		for row in box_array:
			boxes_container = widgets.HBox(row)
			# display(boxes_container)
			group_layout_arr.append(boxes_container)
		
		command_area = widgets.Textarea(
			value='',
			placeholder='Type your commands here',
			layout=Layout(width='auto'),
		)
		command_box = widgets.VBox([command_area,button_box])
		# display(command_box)
		group_layout_arr.append(command_box)
		

	

	#===================================================#
	#-----------------Button-Functions------------------#
	#===================================================#

	def submit_button_clicked(b):
		ssh_list_instances = {}
		for checkbox in box_list:
			if(checkbox.value == True):
				for instance in instances:
					if instance['Instance Id'] == checkbox.description or instance['Name'] == checkbox.description:
						if instance['Service'] in ssh_list_instances:
							ssh_list_instances[instance['Service']].append(instance)
						else:
							ssh_list_instances[instance['Service']] = [instance]
							
		for key in ssh_list_instances:
			for service in cloud_list:
				if key == service.name:
					print(service.name.upper())
					service.ssh(ssh_list_instances[key], command_area.value, False)

	def submit_button_v_clicked(b):
		ssh_list_instances = {}
		for checkbox in box_list:
			if(checkbox.value == True):
				for instance in instances:
					if instance['Instance Id'] == checkbox.description or instance['Name'] == checkbox.description:
						if instance['Service'] in ssh_list_instances:
							ssh_list_instances[instance['Service']].append(instance)
						else:
							ssh_list_instances[instance['Service']] = [instance]

		for key in ssh_list_instances:
			for service in cloud_list:
				if key == service.name:
					print(service.name.upper())
					service.ssh(ssh_list_instances[key], command_area.value, True)
	
	def select_button_clicked(b):
		toggle = check_true(box_list)
		for checkbox in box_list:
			checkbox.value = toggle

	def check_true(box_list):
		if(box_list[0].value):
			for box in box_list:
				if(not box.value):
					return True
			return False
		else:
			for box in box_list:
				if(box.value):
					return True
			return True

	submit_button.on_click(submit_button_clicked)
	submit_button_v.on_click(submit_button_v_clicked)
	select_button.on_click(select_button_clicked)
	return group_layout_arr