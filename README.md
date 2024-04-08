# Amazon Bedrock Generative AI Demo Apps

This project uses [Streamlit](https://streamlit.io/) to build example generative AI applications on AWS with [Amazon Bedrock](https://aws.amazon.com/bedrock/).

- **Product Metadata Generator**: 
Use product images to generate product descriptions, feature lists, and meta tag code for Open Graph, schema.org, and more...
- **Product Review Summarizer**: 
List the most common positive and negative comments from a set of consumer product reviews and summarize the overall sentiment.
- **Product Blog Writer**: 
Generate a 750-1000 word blog post with a comma-separated list of related SEO keywords.
- **Doument FAQ Generator**: 
Use PDF documents to generate a list of expected customer questions and their answers.

## Install 

Follow these steps to install and run this project on AWS using the AWS Cloud9 cloud-based integrated development environment (IDE). 

### Cloud9 Setup

1. Create a new [Cloud9](https://console.aws.amazon.com/cloud9control/home#/create) environment.

   - Name: ```gen-ai-demo```
   - EC2 Instance: ```m5.large``` (recommended)
   - Platform: ```Ubuntu Server 22.04 LTS```

1. Once created, open the new Cloud9 environment.

1. Toggle off AWS managed temporary credential in Cloud9 by going to **Preferences > AWS Settings > Credentials**

1. Configure the AWS CLI with your permanent AWS credentials. You will need an ```AWS Access Key ID``` and ```AWS Secret Access Key``` for the next step.
   - (Optional) [Create an access key](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-iam-create-creds.html) for an IAM user with AdministratorAccess  if you don't already have one.

1. Configure your AWS credentials and region in the Cloud9 terminal using the [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/configure/).

```
aws configure
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

## Customize

Once the app is up and running, you can begin to customize for your own use cases.

1. Edit main entry page content for the app in ```app/Main_Menu.py```.

1. Add your own Streamlit scripts to the ```app/pages``` directory and they will automatically be included in the main menu.

## Clean Up

1. Delete the Cloud9 environment you created.
