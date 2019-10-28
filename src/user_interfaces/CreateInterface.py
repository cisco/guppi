from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display, FileLink
import ipywidgets as widgets

import src.plugins as plugins
import paramiko
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')


#===================================================#
#--------------Create-Interface-Function------------#
#===================================================#
def render_create_interface(cloud_list, cloud_index):

	service = cloud_list[cloud_index]
	if not service.check_setup():
		instances = []
	else:
		instances = service.get_instances_info()

	group_list = ["Create Group"]

	for instance in instances:
		group_name = instance['Group Name']
		if group_name not in group_list and group_name != '':
			group_list.append(group_name)

	group_list.sort(key=str.lower)

	group_dropdown = widgets.Dropdown(
		options = group_list,
		description= "Group: ",
	)
	
	new_group_text = widgets.Text(
		value= '',
		placeholder= 'New Group Name',
		disabled = False
	)

	def on_change(change):
		if(group_dropdown.value == "Create Group"):
			new_group_text.disabled = False
		else:
			new_group_text.disabled = True

	group_dropdown.observe(on_change)

	name_row_arr = [group_dropdown,new_group_text]

	name_row = widgets.HBox(name_row_arr)
	

	size_list = service.get_size_list()
	value = service.get_default_size()

	size_dropdown = widgets.Dropdown(
		options = size_list,
		description= "Size: ",
		value = value,
	)

	num_instances = widgets.BoundedIntText(
		value=1,
		min=1,
		max=20,
		step=1,
		description='How Many?',
		disabled=False
	)

	create_button = widgets.Button(
		description='Create Instance'
	)



	def create_button_clicked(b):
		if(new_group_text.value == '' and group_dropdown.value == 'Create Group'):
			print("Please enter a group name")
		else:
			# def create_instance(self,group,size,region):
			group = group_dropdown.value

			if(group == "Create Group"):
				group = new_group_text.value

			service.create_instance(group,size_dropdown.value,num_instances.value)
		

	create_button.on_click(create_button_clicked)

	size_region_row = [size_dropdown,num_instances]
	sr_row = widgets.HBox(size_region_row)
	if service.check_setup():
		display(name_row)
		display(sr_row)
		display(create_button)
	else:
		fn = "./src/plugins/"+service.name+"Service/"+service.name +"Setup.txt"
		html_as_str = open(fn, 'r').read()
		setup = widgets.HTML(value=html_as_str)
		display(setup)






