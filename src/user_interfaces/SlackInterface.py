# from IPython.core import magic_arguments
# from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
# from IPython.display import HTML, display

# import ipywidgets as widgets
# from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider
# from datetime import datetime

# from slackclient import SlackClient
# import os
# import sys

# token = "xoxp-524358460228-524727397301-562934358338-57f264d9e922b399e56952c65bac020f"
# sc = SlackClient(token)

# #===================================================#
# #---------------Slack-API-Funtions------------------#
# #===================================================#

# def get_channel_list():
# 	channel_list = sc.api_call("channels.list")
# 	if(channel_list.get('ok','')):
# 		channels_info = []
# 		for channel in channel_list['channels']:
# 			channel_data = {
# 				'id': channel.get('id',''),
# 				'name': channel.get('name',''),
# 			}
# 			channels_info.append(channel_data)
# 		return channels_info
# 	else:
# 		print("Could not load channels")
# 		print(channel_list.get('error',''))


# # returns dict with user info
# def user_info():
# 	users_list = sc.api_call("users.list")
# 	users = []
# 	for member in users_list['members']:
# 		profile = member['profile']
# 		user = {
# 			'id': member.get('id',''),
# 			'username': member.get('name',''),
# 			'real_name': profile.get('real_name_normalized','')
# 		}
# 		users.append(user)
# 	return users
		
# # sends a new message to passed in channel_name and message
# def post_message(channel_name, message):
# 	result = sc.api_call(
# 		"chat.postMessage",
# 		channel=channel_name,
# 		text=message,
# 	)
# 	if(result.get('ok','') == True):
# 		print("Message sent to " +channel_name)
# 	else:
# 		print('Message could not be sent')
# 		print(result.get('error',''))

# #pass in userid, returns associated username
# def get_username(user_id, users):
# 	for user in users:
# 		if(user_id == user.get('id','')):
# 			return user.get('real_name','')
# 	return "no username"

# #pass in channel name, returns associated channel id
# def get_channel_id(channel_name):
# 	channels_list = sc.api_call("channels.list")
# 	for channel in channels_list['channels']:
# 		if(channel['name']== channel_name):
# 			return channel['id']
# 	return channel_name + "does not exist"

# #pass in channel_name and number of messages, returns last x messages from channel
# def get_latest_messages(channel_name, users, num_messages):
# 	channel_id = get_channel_id(channel_name)
# 	message_list = sc.api_call(
# 					"channels.history",
# 					channel=channel_id,
# 					count = num_messages,
# 					)
# 	if(message_list.get('ok','') == True):
# 		#replaces userid with users actual name
# 		for message in message_list['messages']:
# 			if('user' in message):
# 				name = get_username(message['user'], users)
# 				message['user'] = name
# 		return message_list['messages']
# 	else:
# 		print('Could not view messages')
# 		print(message_list.get('error',''))
# 		return False

# #===================================================#
# #----------Slack-Interface-Functions----------------#
# #===================================================#

# #takes in channel name, outputs last x messages
# def render_slack_interface():
# 	users = user_info()
# 	channels_info = get_channel_list()
# 	channels_box_list = []
# 	for channel in channels_info:
# 		# gets last 10 messages
# 		messages = get_latest_messages(channel.get('name',''), users, 3)
# 		message_list = []
# 		for message in reversed(messages):
# 			if('user' in message):
# 				username = widgets.HTML(value="<b>"+message['user']+":<b>",layout=Layout(width='25%'))
				
# 				if('bot_id' in message and 'attachments' in message):
# 					if('text' in message['attachments']or 'text' in message['attachments'][0]):
# 						if(message['user'] == 'GitHub'):
# 							message_content = widgets.HTML(value= message['attachments'][0]['text'],layout=Layout(width='70%'))
# 						else:
# 							message_content = widgets.HTML(value= message['attachments']['text'],layout=Layout(width='70%'))
						
			
# 				else:
# 					message_content = widgets.HTML(value= message['text'],layout=Layout(width='70%'))
# 			elif('username' in message):
# 				username = widgets.HTML(value="<b>"+message['username']+":<b>",layout=Layout(width='25%'))
# 				message_content = widgets.HTML(value= message['text'],layout=Layout(width='70%'))
			
# 			ts = float(message['ts'])
# 			formatted_time = datetime.utcfromtimestamp(ts).strftime('%H:%M')
# 			empty_space = widgets.HTML(value= '',layout=Layout(width='5%'))
# 			timestamp = widgets.HTML(value= formatted_time)

# 			box_layout = Layout(
# 				border='solid 1px',
# 				padding='1em',
# 				width= '100%',
# 			)
# 			message_list.append(Box([username,message_content,empty_space,timestamp], layout=box_layout))
		
# 		messages_box = widgets.VBox(message_list)
# 		channels_box_list.append(messages_box)
	
	
# 	accordion = widgets.Accordion(channels_box_list)
# 	acc_index = 0
	
# 	#adding titles to the accordian
# 	for channel in channels_info:
# 		acc_title = channel['name']
# 		accordion.set_title(acc_index, acc_title)
# 		acc_index += 1

# 	display(accordion)

# #takes in channel name and message, sends message to channel
# def send_message(channel,message):
# 		post_message(channel, message)
