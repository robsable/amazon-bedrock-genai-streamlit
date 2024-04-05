# Amazon Bedrock Generative AI Demo Apps

This project uses [Streamlit](https://streamlit.io/) to build examples that demonstrate how [Amazon Bedrock](https://aws.amazon.com/bedrock/) can be used to develop generative AI applications on AWS.

## Install 

Follow these steps to install and run this project. 


### Cloud9 Setup

1. Create a new AWS [Cloud9](https://console.aws.amazon.com/cloud9control/home#/create) environment.

   - Name: ```gen-ai-demo```
   - EC2 Instance: ```m5.large``` (recommended)
   - Platform: ```Ubuntu Server 22.04 LTS```

1. Once created, open the new Cloud9 environment.

1. Toggle off AWS managed temporary credential in Cloud9 by going to **Preferences > AWS Settings > Credentials**

1. Configure the AWS CLI with your permanent AWS credentials. You will need an ```AWS Access Key ID``` and ```AWS Secret Access Key``` for the next step.

1. (Optional) [Create an access key](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-iam-create-creds.html) for an IAM user with AdministratorAccess  if you don't already have one.

1. Configure your credentials in the Cloud9 terminal using the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/configure/).

```
aws configure

AWS Access Key ID []: <ENTER YOUR ACCESS KEY ID>
AWS Secret Access Key []: <ENTER YOUR SECRET ACCESS KEY>
Default region name []: <ENTER YOUR DEFAULT AWS REGION>
Default output format [None]: 
```

### Application Setup

1. Use the integrated Terminal to clone this GitHub repository.

```
git clone https://github.com/robsable/amazon-bedrock-genai-streamlit
cd amazon-bedrock-genai-streamlit
```

2. Install Python requirements.

```
pip3 install -r setup/requirements.txt -U
```

3. Run the Streamlit app.

```
cd app
streamlit run Main_Menu.py --server.port 8080
```
4. In Cloud9, go to the **Preview** menu and select **Preview Running Application**. A new tab in the Cloud9 IDE will open and load your running application.

## Clean Up

1. Delete the Cloud9 environment you created.
