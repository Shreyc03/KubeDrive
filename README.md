# KubeDrive
Too lazy to back up your important files or accidentally deleted something crucial? KubeDrive has you covered.<br> 
This project saves everything in a folder on your local PC to a shared folder on Google Drive.

### Get Started
1. Go to Google Cloud and start a new project.
2. Click on "Enable APIs & Services" and enable the Google Drive API.
3. Go to "Credentials" and create a service account.
4. Create a key and download the service-account-key.json file.
5. Create a new folder in your personal Gmail account, note its ID, and share that folder with the service account by giving it access via its email address.

### Run the project
1. Build and push the Docker image to your repository, then update the image reference in cronjob.yaml or use the image from my public repository.
2. Store sensitive information like the service account credentials and the folder ID using Kubernetes secrets by running the following commands:<br>
`kubectl create secret generic google-service-account-secret --from-file=service-account-key.json`<br>
`kubectl create secret generic google-drive-folder-id-secret --from-literal=FOLDER_ID='{your_folder_id}'`
3. If using docker Desktop in the <b>path</b> line change the path by keeping the same prefix and add the path of the folder whose contents you want to backup after <b>/host</b>
4. Run `kubectl apply -f {yaml_filename}` for all the YAML files in the correct order, and voila! The contents of the folder will be backed up once every week!

