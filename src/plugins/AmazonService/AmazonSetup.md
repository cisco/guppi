# AWS EC2 initial configuration instructions

 If AWS CLI is not installed on your machine, run:
    pip install awscli

1.  Sign in or sign up for AWS [here](https://console.aws.amazon.com/iam/home?#home)

2.  In the navigation pane of the console, choose **Users**

3.  Select your username from the list of users

4.  Navigate to the **security credentials** tab, and choose **create access key**

5.  Click **Create Access Key**, this will give you your **Access Key ID** and **Secret Access Key**

6.  In your terminal, run **aws configure**

7.    * Enter your **Access Key ID**
	  * Enter your **Secret Access Key**
	  * Enter your default region name, you can find your region name [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html)
	  * Enter JSON for default output format

8.  Reload GUPPI