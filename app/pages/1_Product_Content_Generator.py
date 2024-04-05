import streamlit as st
import boto3
import json
import base64
from io import BytesIO


#get a BytesIO object from file bytes
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


#get a base64-encoded string from file bytes
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


#load the bytes from a file on disk
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


#get the stringified request body for the InvokeModel API call
def get_image_understanding_request_body(prompt, image_bytes=None, mask_prompt=None, negative_prompt=None):
    input_image_base64 = get_base64_from_bytes(image_bytes)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg", #this doesn't seem to matter?
                            "data": input_image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    }
    
    return json.dumps(body)



#generate a response using Anthropic Claude
def get_response_from_model(prompt_content, image_bytes, mask_prompt=None):
    session = boto3.Session()
    
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    body = get_image_understanding_request_body(prompt_content, image_bytes, mask_prompt=mask_prompt)
    
    response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-sonnet-20240229-v1:0", contentType="application/json", accept="application/json")
    
    response_body = json.loads(response.get('body').read()) # read the response
    
    output = response_body['content'][0]['text']
    
    return output

st.set_page_config(layout="wide", page_title="Product Content Generator", page_icon="⚙️")

st.title("Product Content Generator")
st.caption("**Instructions:**  (1) Select an image  (2) Choose a prompt template  (3) Customize your prompt  (4) Click Generate")

col1, col2, col3 = st.columns([.20,.20,.6])

prompt_options_dict = {
    "Product Metadata" : "Generate\r\nA comma-separated list of at least 20 keywords and phrases.\r\nA set of Open Graph meta tags code.\r\nAn HTML meta keywords tag.\r\nGoogle schema.org product markup.\r\nImage alt text.\r\n\r\nSeparate each section with a horizontal rule",
    "Product Description": "You are a creative marketing writer. Please write a 100 word description of this product.",
    "Image Description": "Describe this image.",
    "Feature List": "List the features of this product.",
    "Social Media Post": "Write a tweet about this product without additional explanation.",
}

prompt_options = list(prompt_options_dict)

image_options_dict = {
    "Insulation": "./pages/images/insulation.jpg",
    "Red Boat": "./pages/images/boat.jpg",
    "White Boat": "./pages/images/boat2.jpg",
    "Other": "./pages/images/insulation.jpg",
}

image_options = list(image_options_dict)


with col1:

    image_selection = st.radio("**Select an image:**", image_options)
    
    if image_selection == 'Other':
        uploaded_file = st.file_uploader("Select an image", type=['png', 'jpg'], label_visibility="collapsed")
    else:
        uploaded_file = None

with col2:

    if uploaded_file and image_selection == 'Other':
        uploaded_image_preview = get_bytesio_from_bytes(uploaded_file.getvalue())
        st.image(uploaded_image_preview, width=200)
    else:
        st.image(image_options_dict[image_selection], width=200)
    

with col3:

    prompt_selection = st.radio("**Choose a prompt template:**", prompt_options, horizontal=True)
    
    prompt_example = prompt_options_dict[prompt_selection]
    
    prompt_text = st.text_area("Prompt",
        value=prompt_example,
        height=150,
        help="What you want to know about the image.",
        label_visibility="collapsed")
    
    go_button = st.button("Generate", type="primary")
    

if go_button:
    with st.spinner("Processing..."):
        
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
        else:
            image_bytes = get_bytes_from_file(image_options_dict[image_selection])
        
        response = get_response_from_model(
            prompt_content=prompt_text, 
            image_bytes=image_bytes,
        )
    
    st.divider()
    st.subheader("Results")
    st.write(response)

