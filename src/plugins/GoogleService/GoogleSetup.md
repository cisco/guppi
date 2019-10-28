
# Google compute initial configuration instructions

 If Google api client is not installed on your machine run:

    pip install --upgrade google-api-python-client

**To open links in a new tab, hold the ctrl ⌃ key (cmd ⌘ on mac) while clicking the link**
 
1.  Go to the [google cloud console](https://console.cloud.google.com/) and create an account or sign onto your existing one.

2.  Go to the [cloud resource manager](https://console.cloud.google.com/cloud-resource-manager) and select or create a Google Cloud Platform project 
**NOTE: GUPPI will only work if your google account has only one project associated with it**

3.  Ensure that [billing is enabled](https://cloud.google.com/billing/docs/how-to/modify-project) for your Google Cloud Platform Project

4.  Install the [Cloud SDK](https://cloud.google.com/sdk/)

5.  Authenticate your account on your machine
    
    ``gcloud auth application-default login``

6.  Follow google documentation [HERE](https://cloud.google.com/apis/docs/enable-disable-apis?hl=en&ref_topic=6262490&visit_id=636909616876722358-4171110160&rd=1) to enable the Google Cloud Storage API and Cloud Resource Manager API

7.  [Create a storage bucket](https://cloud.google.com/storage/docs/creating-buckets)

8.  Create a [service account for authentication](https://console.cloud.google.com/projectselector/apis/credentials/serviceaccountkey?supportedpurview=project)
    1.  From the Service account list, select **New service account.**
    2.  In the **Service account name field**, enter a name.
    3.  From the **Role list,** select **Project > Owner.**
    4.  Click **Create.** This should download a JSON key
    5.  Create a folder called ``googleCredentials`` in ``project-guppi/src/plugins/GoogleService``, and move the downloaded key into it. The key should end in .json

9.  [Create or locate a SSH key to use with your project](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#createsshkeys)  
Note: When generating the rsa key, ensure that the key comment(username on mac) is the same as your email, with ``. @ -`` symbols replaced with underscores, for example ``user_lastname_gmail_com``.

  Windows: 
 
 Puttygen does not save files in the correct format, so you must manually copy the public key generated in puTTygen (box at top beginning with ssh-rsa). Paste the contents of the private key into a new entry in the SSH Keys section of the [project metadata](https://console.cloud.google.com/compute/metadata/sshKeys) and hit save. To save the private key, in puttygen click **conversions** at the top, then **Export OpenSSH key** and save the file as ``gc_rsa.pem`` and in the ``project-guppi/src/plugins/GoogleService`` folder in guppi. 
 
 Mac/Linux: 
 
 Paste the contents of the private key into a new entry in the SSH Keys section of the [project metadata](https://console.cloud.google.com/compute/metadata/sshKeys) and hit save. Rename the private SSH file to gc_rsa.pem and move it into the ``project-guppi/src/plugins/GoogleService`` folder in guppi.

10.  Open Jupyter Notebook. If you already have guppi open, restart the kernel. Reload the guppi extension. If everything was configured properly you should be able to create, display, and interact with your google compute instances!

Contact katekaho on github if you encounter any problems setting up.
