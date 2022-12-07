from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display

import ipywidgets as widgets
from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
from datetime import datetime

from github import Github
# To work, need to 'pip install PyGithub'

# First create a Github instance:

# using username and password
# g = Github(user, password)

# or using an access token [for security purposes it is removed from this example]

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token"

# Specify Repository Name
repo_name = 'katekaho/project-guppi'


#===================================================#
#---------------Github-API-Funtions-----------------#
#===================================================#

# Return a dict with push events
def get_notifications(num_notifications):
	repo = g.get_repo(repo_name)
	events = repo.get_events()
	counter = 0
	notifications = []
	base = 'https://github.com/' + repo_name + '/'
	commit_base = base + 'commit/'
	branch_base = base + 'tree/'
	for event in events:
		counter = counter + 1
		if counter > num_notifications:
			break
		commitData = []
		recent_commit_url = ''
		branch = ''
		first = True

		if event.type == 'PushEvent':
			branch = event.payload.get('ref').rsplit('/', 1)[-1]
			for commit in event.payload.get('commits'):
				if first == True:
					recent_commit_url = commit_base + commit['sha']
					first = False
				c = {
					'sha': commit['sha'],
					'message': commit['message'],
					'url': commit_base + commit['sha']
				}
				commitData.append(c)
		format_event = {
			'created_at': event.created_at,
			'user': event.actor.login,
			'user_img': event.actor.avatar_url,
			'user_url': event.actor.html_url,
			'type': event.type,
			'size': event.payload.get('size'),
			'branch': branch,
			'branch_url': branch_base + branch,
			'commits': commitData,
			'recent_commit_url': recent_commit_url,
			'repo_name': base
		}
		notifications.insert(0, format_event)
	return notifications

#===================================================#
#---------------Github-Magic-Class------------------#
#===================================================#

# @magics_class
# class GithubMagic(Magics):
	
# Gets number to display and displays most recent push events
def display_notifications(num_notifications):
	
	notifications = get_notifications(num_notifications)

	base = 'https://github.com/' + repo_name + '/'

	for n in notifications:
		if n['type'] == 'PushEvent':
			box_layout = Layout(
				border='solid 1px',
				padding='1em',
				flex_flow='column'
			)

			div = "<div>"
			div_end = "</div>"
			a = "<a href="
			a_end = "</a>"
			img = "<img src="
			close = ">"
			end = "/>"

			profile_info = div + a + n['user_url'] + close + img + n['user_img'] + end 
			profile_info = profile_info + n['user'] + a_end + div_end

			commit_info = div + a + n['recent_commit_url'] + close + str(n['size']) + ' new commit'
			if n['size'] > 1:
				commit_info = commit_info + 's'
			commit_info = commit_info + a_end + ' pushed to '
			commit_info = commit_info + a + n['branch_url'] + close + n['branch'] + a_end + div_end

			all_commits = div
			for commit in n['commits']:
				all_commits = all_commits + div + a + commit['url'] + close + commit['sha'][:8]
				all_commits = all_commits + a_end + ' - ' + commit['message'] + div_end

			timestamp = div + str(n['created_at']) + div_end

			project_info = div + a + base + close + repo_name + a_end + div_end


			time = widgets.HTML(value=timestamp, layout=Layout(width="40%"))
			profile_i = widgets.HTML(value=profile_info, layout=Layout(width="10%"))
			commit_i = widgets.HTML(value=commit_info, layout=Layout(width="100%"))
			all_c = widgets.HTML(value=all_commits, layout=Layout(width="100%"))
			project_i = widgets.HTML(value=project_info, layout=Layout(width="100%"))

			message_box = Box([time, profile_i, commit_i, all_c, project_i], layout=box_layout)
			display(message_box)

# 	# Takes in jupyter inputs 
# 	@line_magic
# 	@magic_arguments.magic_arguments()
# 	@magic_arguments.argument('arguments', nargs='*')
# 	def github(self, line=''):
# 		args = magic_arguments.parse_argstring(self.github, line)
# 		if(len(args.arguments) == 1 and args.arguments[0].isdigit()):
# 	  		self.display_notifications(int(args.arguments[0]))
# 		elif(len(args.arguments) == 1 and args.arguments[0] == 'help'):
# 			print("To view github push events:\n%github [number of recent to view] \n\n")
# 		else:
# 			print("For usage, use the  %github help command")

# #===================================================#
# #-----------ipython-Magic-Registering---------------#
# #===================================================#

# def load_ipython_extension(ipython):
# 	"""This function is called when the extension is
# 	loaded. It accepts an IPython InteractiveShell
# 	instance. We can register the magic with the
# 	`register_magic_function` method of the shell
# 	instance."""
# 	ipython.register_magics(GithubMagic)
