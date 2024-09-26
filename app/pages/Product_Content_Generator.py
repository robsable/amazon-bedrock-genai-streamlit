import streamlit as st
import boto3
import json
import base64
from io import BytesIO
from datetime import datetime, timezone, timedelta
from pages.lib import models_shared

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
def get_request_body(prompt, image_bytes=None, mask_prompt=None, negative_prompt=None):
    input_image_base64 = get_base64_from_bytes(image_bytes)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,
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
def get_response_from_model(model_id, prompt_content, image_bytes, mask_prompt=None):
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    body = get_request_body(prompt_content, image_bytes, mask_prompt=mask_prompt)
    response = bedrock.invoke_model(body=body, modelId=model_id, contentType="application/json", accept="application/json")
    response_body = json.loads(response.get('body').read()) # read the response
    output = response_body['content'][0]['text']
    return output

#################
# Streamlit App #
#################
st.set_page_config(layout="wide", page_title="Product Content Generator", page_icon=":gear:")

st.title("Generate Product Content")
st.caption("**Instructions:**  (1) Select an image  (2) Choose a prompt template  (3) Customize your prompt  (4) Click Generate")

col1, col2 = st.columns([.3,.7])

prompt_options_dict = {
    "Product Metadata" : "Generate\r\nA comma-separated list of at least 20 keywords and phrases.\r\nA set of Open Graph meta tags code.\r\nAn HTML meta keywords tag.\r\nGoogle schema.org product markup.\r\nImage alt text.\r\n\r\nSeparate each section with a horizontal rule",
    "Product Description": "You are a creative marketing writer. Please write a 100 word description of this product.",
    "Image Description": "Describe this image.",
    "Feature List": "List the features of this product.",
    "Social Media Post": "Write a tweet about this product without additional explanation.",
}

prompt_options = list(prompt_options_dict)

image_options_dict = {
    "Insulation": "./static/insulation.jpg",
    "Red Boat": "./static/boat.jpg",
    "White Boat": "./static/boat2.jpg",
    "Other": "./static/blank.jpg",
}

image_options = list(image_options_dict)

# Get Bedrock LLM Models options
model_options = list(models_shared.vision_model_options_dict)

with col1:

    image_selection = st.radio("**Select an image:**", image_options)
    
    if image_selection == 'Other':
        uploaded_file = st.file_uploader("Select an image", type=['png', 'jpg'], label_visibility="collapsed")
    else:
        uploaded_file = None

    if uploaded_file and image_selection == 'Other':
        uploaded_image_preview = get_bytesio_from_bytes(uploaded_file.getvalue())
        st.image(uploaded_image_preview, width=200)
    else:
        st.image(image_options_dict[image_selection], width=200)
    

with col2:

    prompt_selection = st.radio("**Choose a prompt template:**", prompt_options, horizontal=True)
    
    prompt_example = prompt_options_dict[prompt_selection]
    
    prompt_text = st.text_area("Prompt",
        value=prompt_example,
        height=150,
        help="What you want to know about the image.",
        label_visibility="collapsed")
    
    selected_model = st.radio("**Select a model:**", 
        model_options,
        format_func=models_shared.get_vision_model_label,
        horizontal=True
    )
    
    go_button = st.button("Generate", type="primary")
    

if go_button:
        
    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
    else:
        image_bytes = get_bytes_from_file(image_options_dict[image_selection])

    st.divider()
    st.subheader("Content")
    st.write("**GENERATED BY:** "+selected_model)

    timezone_offset = -4.0  # Eastern Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))

    start = datetime.now(tzinfo)

    with st.spinner("Processing..."):
        response = get_response_from_model(
            model_id=selected_model,
            prompt_content=prompt_text, 
            image_bytes=image_bytes,
        )
    
    end = datetime.now(tzinfo)

    st.write("**TIME TO GENERATE** = " + str(end - start))
    st.write(response)

