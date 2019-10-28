import boto3
import random
import paramiko
import threading
from ..pluginbase import PluginBase

class LocalBaseClass:
	pass
@PluginBase.register
class AmazonService(LocalBaseClass):
	def __init__(self):
		self.type = "AWS SERVICE"
		self.name = "Amazon"
		self.configured = True
		try:
			self.ec2 = boto3.resource('ec2')
		except Exception :
			print("AWS CLI config error: Unable to retrieve boto3 resource")
			self.configured = False

		try:
			self.ec2_client = boto3.client('ec2')
		except Exception :
			print("AWS CLI config error: Unable to retrieve boto3 client")
			self.configured = False

		if(self.configured):
			self.formatted_instances = self.get_instances_info()
	
	def check_setup(self):
		#comment this to show instructions
		return self.configured
		
	def create_instance(self,group,size,num):
		tags = [
			# {'Key':'Name','Value': group + str(random.randint(10000,99999))},
			{'Key':'Group','Value': group},
		]

		tag_specification = [{'ResourceType': 'instance', 'Tags': tags},]

		new_instances = self.ec2.create_instances(
			ImageId='ami-082c116bf79a9feef',
			MinCount=num,
			MaxCount=num,
			InstanceType= size,
			KeyName='key',
			TagSpecifications= tag_specification,
		)

		for instance in new_instances:
			self.ec2.create_tags(Resources = [instance.instance_id], Tags=[{'Key': 'Name', 'Value': self.name + '-' + instance.instance_id[-4:]}])
		
		if num == 1:
			print("Instance Created.")
		elif num > 1:
			print("Instances Created.")
	
	def get_instances_info(self):
		response = self.ec2_client.describe_instances()
		reservations = response.get('Reservations')
		instances = []

		for reservation in reservations:
			reservationInstances = reservation.get('Instances')
			for inst in reservationInstances:
				instances.append(inst)

		instancesFormatted = []

		for instance in instances:
			tags = instance.get('Tags', [])
			name = ''
			group_name = ''
			for tag in tags:
				tagKey = tag.get('Key', '')
				if tagKey == 'Name':
					name = tag['Value']
				elif tagKey == 'Group':
					group_name = tag['Value']

			placement = instance['Placement']
			availabilityZone = placement['AvailabilityZone']

			state = instance['State']
			stateName = state.get('Name', '')

			launchTime = instance.get('LaunchTime', '')

			dns = instance.get('PublicDnsName','')

			if(dns == ''):
				dns = "Instance is offline"

			if len(name) > 20:
				name = name[:20] + '...'

			formatInst = {
				'Name': name,
				'Service' : self.name,
				'Instance Id': instance.get('InstanceId', ''),
				'Instance Type': instance.get('InstanceType', ''),
				'Availability Zone': availabilityZone,
				'State': stateName,
				'Key Name': instance.get('KeyName', ''),
				'Launch Time': launchTime,
				'Dns': dns,
				'Group Name': group_name

			}

			instancesFormatted.append(formatInst)

		return instancesFormatted

	def terminate_instance(self,index):
		print("Terminating AWS Instance...")
		instances = self.get_instances_info()
		ids = [instances[index]['Instance Id']]
		self.ec2.instances.filter(InstanceIds=ids).terminate()
		# recalibrate self.formatted_instances to reflect the change
		self.formatted_instances = self.get_instances_info()
		print("AWS Instance Terminated.")
		print("Rerun %guppi cloud to update.")

	def toggle_instance(self,index):
		instances = self.get_instances_info()
		ids = [instances[index]['Instance Id']]

		current_state = instances[index]['State']
		if(current_state == "running"):
			print("Stopping AWS Instance...")
			self.ec2.instances.filter(InstanceIds=ids).stop()
			print("AWS Instance Stopped.")
			print("Rerun %guppi cloud to update.")

		elif(current_state == "stopped"):
			print("Starting AWS Instance...")
			self.ec2.instances.filter(InstanceIds=ids).start()
			print("AWS Instance Started.")
			print("Rerun %guppi cloud to update.")
		else:
			print("Instance has already been toggled")
			print("Rerun %guppi cloud to reflect changes")
		# recalibrate self.formatted_instances to reflect the change
		self.formatted_instances = self.get_instances_info()

	def reboot_instance(self,index):
		print("Rebooting AWS Instance...")
		instances = self.get_instances_info()
		state = instances[index]['State']
		if(state == "running"):
			ids = [instances[index]['Instance Id']]
			self.ec2.instances.filter(InstanceIds=ids).reboot()
			# recalibrate self.formatted_instances to reflect the change
			self.formatted_instances = self.get_instances_info()
			print("AWS Instance Rebooted.")
			print("Rerun %guppi cloud to update.")
		else:
			print("Please rerun %guppi cloud to reflect changes")
			print("You can only reboot instances that are  \"Running\" ")

	def update_group(self, instance_id, group_name):
		self.ec2.create_tags(
			Resources=instance_id,
			Tags=[
				{
					'Key': 'Group',
					'Value': group_name
				}
			]
		)
		# print("Please refresh cell to reflect change.")
	
	def ssh(self, instances, commands, verbose):
		# clear_output()
		# print("Running, please wait...")
		
		# threadOutputList contains list of all shell outputs
		threadOutputList = []
		
		# threadErrorList contains list of all shell errors
		threadErrorList = []
		
		# sshThread gets called by each thread
		def sshThread(commands, instanceId):
			# set the dns for each instance
			Dns = ''
			for vm in instances:
				if(instanceId == vm['Instance Id'] or instanceId == vm['Name']):
					Dns = vm['Dns']
			
			# ssh in and run commands
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			user_and_key = self.get_user_and_keyname()

			ssh.connect(Dns,
						username=user_and_key[0],
						key_filename=user_and_key[1])
		
			stdin, stdout, stderr = ssh.exec_command(commands)
			stdin.flush()
			
			# create list of all lines of output
			outputList = []
			outputList.append("=======================================================")
			outputList.append(instanceId)
			outputList.append("=======================================================")
			for line in stdout.read().splitlines():
				outputList.append(line.decode('ascii'))
			# create list of all lines of errors
			errorList = []
			errorList.append("=======================================================")
			errorList.append(instanceId)
			errorList.append("=======================================================")
			errorOutput = stderr.read().splitlines()
			splitCommands = commands.split(";")
			for command in splitCommands:
				if command.strip() == "":
					splitCommands.remove(command)
			numOfCommands = len(splitCommands)
			
			# if no errors append "successfully run" to output and error lists
			if len(errorOutput) == 0:
				if numOfCommands == 1:
					errorList.append("Successfully ran 1 command\n")
					outputList.append("Successfully ran 1 command\n")
				else:
					errorList.append("Successfully ran " + str(numOfCommands) + " commands\n")
					outputList.append("Successfully ran " + str(numOfCommands) + " commands\n")
			
			# append errors to the errorList
			for line in errorOutput:
				errorList.append(line.decode('ascii'))
			# append errorList to threadErrors
			threadErrorList.append(errorList)

			# append outputList to the threadOutputs
			threadOutputList.append(outputList)
			
			# disconnect from instance
			ssh.close()
		
		# theadList will contain a thread for each instance
		threadList = []
		
		# for each checked instance create a thread
		for instance in instances:
			thread = threading.Thread(target=sshThread, args=(commands, instance['Instance Id'])) 
			thread.start()
			threadList.append(thread)

		# wait for each thread to finish
		for thread in threadList:
			thread.join()
		
		# if verbose flag is used print output from each instance shell
		if verbose:		
			for data in threadOutputList:
				for output_line in data:
					print(output_line)
		# else just print errors from each instance shell
		else:
			for errors in threadErrorList:
				for output_line in errors:
					print(output_line)
	
	def get_size_list(self):
		return ['t2.nano', 't2.micro', 't2.small', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 'm5d.large', 'm5d.xlarge', 'm5d.2xlarge', 'm5d.4xlarge', 'm5d.12xlarge', 'm5d.24xlarge',  'm5.large', 'm5.xlarge', 'm5.2xlarge', 'm5.4xlarge', 'm5.12xlarge', 'm5.24xlarge', 'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge', 'c5d.large', 'c5d.xlarge', 'c5d.2xlarge', 'c5d.4xlarge', 'c5d.9xlarge', 'c5d.18xlarge', 'c5.large', 'c5.xlarge', 'c5.2xlarge', 'c5.4xlarge', 'c5.9xlarge', 'c5.18xlarge', 'c4.large', 'c4.xlarge', 'c4.2xlarge', 'c4.4xlarge', 'c4.8xlarge', 'g2.2xlarge', 'g2.8xlarge', 'g3.4xlarge', 'g3.8xlarge', 'g3.16xlarge', 'r5d.large', 'r5d.xlarge', 'r5d.2xlarge', 'r5d.4xlarge', 'r5d.12xlarge', 'r5.large', 'r5.xlarge', 'r5.2xlarge', 'r5.4xlarge', 'r5.12xlarge', 'r5.24xlarge', 'r4.large', 'r4.xlarge', 'r4.2xlarge', 'r4.4xlarge', 'r4.8xlarge', 'r4.16xlarge', 'z1d.large', 'z1d.xlarge', 'z1d.2xlarge', 'z1d.3xlarge', 'z1d.6xlarge', 'z1d.12xlarge', 'd2.xlarge', 'd2.2xlarge', 'd2.4xlarge', 'd2.8xlarge', 'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge', 'i3.large', 'i3.xlarge', 'i3.2xlarge', 'i3.4xlarge', 'i3.8xlarge', 'i3.16xlarge', 'i3.metal']
	
	def get_default_size(self):
		return 't2.micro'
	
	def get_user_and_keyname(self):
		return ['ec2-user', './src/plugins/AmazonService/key.pem']
