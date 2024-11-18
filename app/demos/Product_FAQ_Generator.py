import streamlit as st
import boto3
from botocore.exceptions import ClientError
import PyPDF2
import io
from datetime import datetime, timezone, timedelta

st.set_page_config(layout="wide", page_title="Product FAQ Writer", page_icon="❓")

st.title("Product FAQ Generator")
st.caption("**Instructions:**  (1) Upoad PDF files  (2) Customize the system prompt  (3) Customize the user prompt  (4) Click Generate")

# Create a Bedrock Runtime client
@st.cache_resource
def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name="us-east-1")

client = get_bedrock_client()

# Set the model ID
model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"


st.sidebar.header("System Prompt")
system_prompt = st.sidebar.text_area(
    "Context and instructions:",
    "You are a helpful AI assistant. Please provide informative and accurate responses. Use emojis whenever possible.",
    height=200
)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# File uploader for PDFs
uploaded_files = st.file_uploader("Upload PDF files for context", type="pdf", accept_multiple_files=True)

# Extract text from uploaded PDFs
pdf_texts = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_text = extract_text_from_pdf(uploaded_file)
        pdf_texts.append(pdf_text)

# Combine PDF texts
combined_pdf_text = "\n\n".join(pdf_texts)

# Display uploaded PDF content
if pdf_texts:
    st.sidebar.header("Uploaded PDFs")
    for i, text in enumerate(pdf_texts):
        with st.sidebar.expander(f"PDF {i+1} Content"):
            st.write(text)

# User input
user_message = st.text_area("User Prompt:", 
                            """Generate the following product marketing content based on the details in the attached documents. All details should be informative and accurate. Separate each section with a horizontal rule.
  - A list of Consumer FAQs with answers to questions consumers in simple to understand terms
  - A list of Installer FAQs with answers to questions installers using technical terms and explanations from product documentation
""",
                            height=200)

gen_button = st.button("Generate", type="primary")


# Button to generate content
if gen_button:
    # Prepare the conversation with PDF context
    conversation = [
        {
            "role": "user",
            "content": [{"text": f"{system_prompt}\n{user_message}\nHere is some context from uploaded PDF files:\n\n{combined_pdf_text}"}],
        }
    ]

    st.write("**GENERATED BY:** "+model_id)

    timezone_offset = -4.0  # Eastern Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))

    start = datetime.now(tzinfo)

    try:
        with st.spinner("Generating response..."):
            # Send the message to the model
            response = client.converse(
                modelId=model_id,
                messages=conversation,
                inferenceConfig={"maxTokens": 2000, "temperature": 1},
                additionalModelRequestFields={"top_k": 250}
            )

            end = datetime.now(tzinfo)
            st.write("**TIME TO GENERATE** = " + str(end - start))
            # Extract and display the response text
            response_text = response["output"]["message"]["content"][0]["text"]
            st.subheader("Response:")
            st.write(response_text)

    except ClientError as e:
        st.error(f"ClientError: Can't invoke '{model_id}'. Reason: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Add some information about the app
# st.sidebar.header("About This App")
# st.sidebar.info(
#     "This Streamlit app uses the AWS Bedrock Runtime to communicate with Claude 3 Sonnet. "
#     "You can upload PDF files to provide context for your conversation. "
#     "Enter your message in the text area and click 'Send Message' to get a response."
# )
