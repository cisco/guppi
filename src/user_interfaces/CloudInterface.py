from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink, clear_output
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider

#===================================================#
#--------------SSH-Interface-Function---------------#
#===================================================#
def render_cloud_interface(cloud_list, cloud_index):
	service = cloud_list[cloud_index]
	service_name = service.type
	if cloud_index < 0:
		service_name = "MultiCloud"
	title = widgets.HTML("<h4>"+service_name+" Instances</h4>")
	display(title)

	instances = []

	#multicloud adds all instances to instance list and appends index
	instDict = {}
	if cloud_index < 0:
		for cloud in cloud_list:
			if cloud.check_setup():
				instDict[cloud.name] = cloud.get_instances_info()
				ind = 0
				for info in instDict[cloud.name]:
					info['index'] = ind
					instances.append(info)
					ind+=1
	else:
		if cloud_list[cloud_index].check_setup():
			instances = cloud_list[cloud_index].get_instances_info()
			ind = 0
			for info in instances:
				info['index'] = ind
				ind+=1

	group_list = []
	
	#filling group tabs
	for instance in instances:
		group_name = instance['Group Name']
		if group_name not in group_list and group_name != '':
			group_list.append(group_name)

	group_list.sort(key=str.lower)
	tab_arr = []
	layout_arr = render_group(service,instances,'multi', cloud_list,cloud_index)
	
	tab_child = widgets.VBox(layout_arr)
	tab_arr.append(tab_child)

	#multicloud addding separate cloud tabs
	if cloud_index < 0:
		c_index = 0
		start_index = 0
		for cloud in cloud_list:
			if cloud.check_setup():
				service_length = len(instDict[cloud.name])
				cloud_instances = instances[start_index:start_index + service_length]
				cloud_layout_arr = render_group(cloud_list[c_index],cloud_instances,'service_group', cloud_list,cloud_index)
				child = widgets.VBox(cloud_layout_arr)
				tab_arr.append(child)
				start_index += service_length
				c_index += 1
			else:
				cloud_instances = []
				cloud_layout_arr = render_group(cloud_list[c_index],cloud_instances,'service_group', cloud_list,cloud_index)
				child = widgets.VBox(cloud_layout_arr)
				tab_arr.append(child)
				c_index += 1
			
	tab = widgets.Tab()

	#appending groups to the tab array
	for group_name in group_list:
		layout_arr = render_group(service,instances,group_name, cloud_list,cloud_index)
		tab_child = widgets.VBox(layout_arr)
		tab_arr.append(tab_child)
	
	tab.children = tab_arr
	tab.set_title(0,'All Instances')
	
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

#renders the accordion for each group
def render_group(service,instances, group_name, cloud_list,cloud_index):
	if group_name == "multi":
		missing = True
		for cloud in cloud_list:
			if cloud.check_setup():
				missing = False
		if cloud_index < 0 :
			if missing:
				setup = widgets.HTML("<h3>No Cloud Service has been setup</h3>")
				return [setup]
		else:
			if not service.check_setup():
				fn = "./src/plugins/"+service.name+"Service/"+service.name +"Setup.txt"
				html_as_str = open(fn, 'r').read()
				setup = widgets.HTML(value=html_as_str)
				return [setup]
	else:
		if not service.check_setup():
			if group_name == "service_group":
				fn = "./src/plugins/"+service.name+"Service/"+service.name +"Setup.txt"
				html_as_str = open(fn, 'r').read()
				setup = widgets.HTML(value=html_as_str)
				return [setup]

	empty = True
	for instance in instances:
		if instance['State'] != 'terminated':
			empty = False
			break

	if empty:
		if group_name == 'multi':
			title = widgets.HTML("<h4> There are no running instances</h4>")
			help_title = widgets.HTML("<h4> Use \"%guppi cloud [SERVICE NAME] create\" to create instances</h4>")
		elif group_name == 'service_group':
			title = widgets.HTML("<h4> There are no running "+service.name+" instances</h4>")
			help_title = widgets.HTML("<h4> Use \"%guppi cloud "+service.name.lower()+" create\" to create "+service.name.lower()+" instances</h4>")
		else:
			title = widgets.HTML("<h4> There are no running instances in "+group_name+"</h4>")
			help_title = widgets.HTML("<h4> Use \"%guppi cloud [SERVICE NAME] create\" to create instances</h4>")


		return [title,help_title]
	group_widget_list = []

	accordion_children = []
	index = 0

	for instance in instances:
		if (instance['Group Name'] == group_name or group_name == 'multi' or group_name == 'service_group'):
			if instance['State'] != 'terminated':
				accordion_child = render_instance_info(service, instance, index, instances, cloud_list)
				accordion_children.append(accordion_child)
		index += 1

	accordion = widgets.Accordion(accordion_children)

	acc_index = 0
				
	#adding titles to the accordian
	for row in instances:
		if row['Group Name'] == group_name or group_name == 'multi' or group_name == 'service_group':
			if row['State'] != 'terminated':
				acc_title = row['Service']
				acc_title += " | "
				if group_name == 'multi' or group_name == 'service_group':
					acc_title += row['Group Name']
					acc_title += " | "
				if row['Name'] == '':
					acc_title += row['Instance Id']
				else:
					acc_title += row['Name']
				acc_title += " | "
				acc_title += row['State']
				
				
				accordion.set_title(acc_index, acc_title)
				acc_index += 1

	group_widget_list.append(accordion)

	return group_widget_list

#renders instance info per each accordion item
def render_instance_info(service, instance_info, index, instances, cloud_list):
	

	#appends all info into array of labels
	info1 = ["<b>Instance ID:</b>", instance_info['Instance Id'] ,"<b>Instance Type:</b>", instance_info['Instance Type'] ,"<b>Availability Zone:</b>", instance_info['Availability Zone'],"<b>Group:<b>"]

	info2 = ["<b>State:<b>" , instance_info['State'], "<b>Public DNS:<b>", instance_info['Dns']]

	#makes each label html and puts into HBox
	items1 = [widgets.HTML(str(i)) for i in info1]
	

	items2 = [widgets.HTML(str(i)) for i in info2]
	instance_info2 = widgets.HBox(items2)

	group_list = []

	for instance in instances:
		if instance['Group Name'] not in group_list:
			group_list.append(instance['Group Name'])
	
	#group dropdown
	group_dropdown = widgets.Dropdown(
		options = group_list,
		value=instance_info['Group Name'],
		disabled=False,
		layout=widgets.Layout(width='20%'),
	)
	items1.append(group_dropdown)

	instance_info1 = widgets.HBox(items1)

	instance_list = []
	instance_list.append(instance_info['Instance Id'])

	
	#buttons
	if(instance_info['State'] == "running"): 
		toggle_button = widgets.Button(description='Stop Instance')
	elif(instance_info['State'] == "stopped"):
		toggle_button = widgets.Button(description='Start Instance')
	else:
		toggle_button = widgets.Button(description='Start Instance',disabled=True)

	#disables the terminate button when not running or stopped
	if(instance_info['State'] == "running" or instance_info['State'] == "stopped"):
		terminate_button = widgets.Button(description='Terminate Instance')
	else:
		terminate_button = widgets.Button(description='Terminate Instance',disabled=True)
	# reboot button
	if(instance_info['State'] == "running"):
		reboot_button = widgets.Button(description='Reboot Instance')
	else:
		reboot_button = widgets.Button(description='Reboot Instance',disabled=True)


	file = open("src/icons/running.png", "rb")

	if(instance_info['State'] == "running"):
		file = open("src/icons/running.png", "rb")
	elif(instance_info['State'] == "pending"or instance_info['State'] == 'staging'):
		file = open("src/icons/pending.png", "rb")
	elif(instance_info['State'] == "stopping"):
		file = open("src/icons/stopping.png", "rb")
	elif(instance_info['State'] == "stopped"):
		file = open("src/icons/stopped.png", "rb")
	elif(instance_info['State'] == "shutting-down"):
		file = open("src/icons/shutting-down.png", "rb")
	else:
		file = open("src/icons/terminated.png", "rb")

	image = file.read()
	indicator = widgets.Image(value=image,format='png')

	buttons = [toggle_button,reboot_button,terminate_button,indicator]
	button_box = widgets.HBox(buttons)

	#puts info and buttons into vBox
	instance_box = widgets.VBox([instance_info1, instance_info2, button_box])

	#===================================================#
	#-----------------Button-Functions------------------#
	#===================================================#
	#terminate instance button handler
	def terminate_button_clicked(b):
		for service in cloud_list:
			if(instance_info['Service'] == service.name):
				service.terminate_instance(instance_info['index'])
		# refresh cell
		# clear_output()
		# render_cloud_interface(cloud_list, 0)


	#toggle instance button handler
	def toggle_button_clicked(b):
		for service in cloud_list:
			if(instance_info['Service'] == service.name):
				service.toggle_instance(instance_info['index'])

	#reboot instance button handler
	def reboot_button_clicked(b):
		for service in cloud_list:
			if(instance_info['Service'] == service.name):
				service.reboot_instance(instance_info['index'])
		# refresh cell
		# clear_output()
		# render_cloud_interface(cloud_list, 0)

	def on_change(change):
		for service in cloud_list:
			if(instance_info['Service'] == service.name):
				service.update_group(instance_list, group_dropdown.value)
		print("Changed group to " + group_dropdown.value)
		print("Rerun %guppi cloud to display")

	group_dropdown.observe(on_change, names='value')

	toggle_button.on_click(toggle_button_clicked)
	terminate_button.on_click(terminate_button_clicked)
	reboot_button.on_click(reboot_button_clicked)

	return instance_box