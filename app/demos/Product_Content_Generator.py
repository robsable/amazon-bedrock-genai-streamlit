import streamlit as st
import boto3
from botocore.exceptions import ClientError
import PyPDF2
import io
from datetime import datetime, timezone, timedelta
from utils import models_shared

#################
# Streamlit App #
#################

# Get Bedrock LLM Models options
model_options = list(models_shared.model_options_dict)

st.set_page_config(layout="wide", page_title="Product Content Generator", page_icon="❓")

st.title("Product Content Generator")
st.caption("**Instructions:**  (1) Upoad PDF files (2) Choose a system prompt and customize if needed (3) Choose a user prompt and customize if needed (4) Adust LLM Parameters as needed (5) Click Generate")

# Create a Bedrock Runtime client
@st.cache_resource
def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name="us-east-1")

client = get_bedrock_client()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

system_prompt_options_dict = {
"Blank" : "",
"😎 AI Assistant" : "You are a helpful AI assistant. Please provide informative and accurate responses. Use emojis whenever possible.",
"Pirate Assistant" : "You are a helpful AI assistant. Please provide informative and accurate responses. Talk like a pirate.",
"Pro Blogger" : """<system_role>You are a professional blog writer with expertise in creating engaging, well-researched content on various topics. Your writing style is informative yet conversational, and you excel at breaking down complex subjects into easily digestible content for a general audience.</system_role>

<task_description>Write a comprehensive, engaging blog post on the given topic. Your post should be well-structured, informative, and tailored to a general audience interested in learning more about the subject.</task_description>

<input_variables>
Topic for the blog post: {uploaded_files}
</input_variables>

<instructions>
1. Research the given topic thoroughly, ensuring you have a solid understanding of the subject matter.
2. Create an outline for the blog post, including main points and potential subheadings.
3. Write an attention-grabbing introduction that hooks the reader and clearly states the post's purpose.
4. Develop the main body of the post with relevant subheadings, incorporating the following:
   - Clear explanations of key concepts
   - Relevant examples or case studies
   - Data or statistics to support your points (with proper citations)
   - Addressing potential questions or concerns the reader might have
5. Conclude the post with a summary of key takeaways and a thought-provoking call-to-action or question for the reader.
6. Review and refine the content for clarity, coherence, and engagement. Ensure a logical flow of ideas throughout the post.
7. Add a catchy title that accurately reflects the content and entices readers to click.
</instructions>

<example>
Here's an example of a well-structured blog post on "The Impact of Artificial Intelligence on Modern Healthcare":

# "AI in Healthcare: Revolutionizing Patient Care and Medical Research"

## Introduction
Artificial Intelligence (AI) is no longer confined to science fiction novels or futuristic movies. It's here, and it's making waves in one of the most critical sectors of our society: healthcare. From diagnosing diseases to developing new drugs, AI is revolutionizing the way we approach medicine and patient care. In this post, we'll explore the transformative impact of AI on modern healthcare and what it means for patients and medical professionals alike.

## AI in Medical Diagnosis
[Content explaining how AI is being used in medical diagnosis, with specific examples and statistics]

## Drug Discovery and Development
[Information on how AI is accelerating the process of drug discovery and development]

## Personalized Treatment Plans
[Discussion on how AI is enabling more personalized treatment plans for patients]

## Streamlining Administrative Tasks
[Explanation of how AI is helping to reduce administrative burden in healthcare settings]

## Challenges and Ethical Considerations
[Balanced view of the challenges and ethical considerations surrounding AI in healthcare]

## Summary
As we've seen, AI is not just changing healthcare; it's revolutionizing it. From more accurate diagnoses to personalized treatment plans, the potential benefits are enormous. However, as with any transformative technology, we must approach AI in healthcare with both excitement and caution. As we move forward, it will be crucial to address the challenges and ethical considerations to ensure that AI truly serves the best interests of patients and healthcare providers alike.

What are your thoughts on AI in healthcare? Do you see it as a game-changer, or do you have concerns? Share your opinions in the comments below!
</example>

<output>
<thinking>
1. Analyze the given topic: {uploaded_files}
2. Research key points, statistics, and examples related to the topic
3. Develop an outline with main sections and subheadings
4. Draft an engaging introduction that hooks the reader
5. Write the main body, ensuring each section flows logically
6. Use bold headings and lists to communicate your points clearly. 
7. Embed as many hyperlinks as possible in the article to resources you are citing. 
8. Craft a conclusion that summarizes key points and encourages reader engagement
9. Review and refine the content for clarity, coherence, and style
10. Create a catchy, relevant title for the blog post
11. Include a comma-separated list of applicable SEO keywords below the article.
</thinking>

<blog_post>
[The final blog post will be written here, following the structure and guidelines provided in the instructions and example]
</blog_post>
</output>
""",
}
system_prompt_options = list(system_prompt_options_dict)


user_prompt_options_dict = {
    "Product FAQ" : """Generate the following product marketing content based on the details in the attached documents. All details should be informative and accurate. Separate each section with a horizontal rule.
    - A list of at least 20 Consumer FAQs with answers to questions consumers in simple to understand terms
    - A list of at least 20 Installer FAQs with answers to questions installers using technical terms and explanations from product documentation
    """,

    "Product Metadata" : """Generate the following product marketing content based on the details in the attached documents. All details should be informative and accurate. Separate each section with a horizontal rule.
  - A comma-separated list of at least 20 keywords and phrases
  - A set of Open Graph meta tags code
  - An HTML meta keywords tag
  - Google schema.org product markup
  - Image alt text markup (up to 120 characters)""",

    "Product Blog": "Write a product blog post.",

    "Product Description": "You are a creative marketing writer. Please write a 100 word description of this product.",

    "Feature List": "List the features of this product.",

    "Social Media Post": "Write a tweet about this product without additional explanation.",
}
user_prompt_options = list(user_prompt_options_dict)

# Sidebar info
with st.sidebar:
    st.markdown("## LLM Parameters")

    with st.container():
        selected_model = st.selectbox("**Model Name**", 
            model_options,
            format_func=models_shared.get_model_label
        )

        MAX_TOKENS = st.slider("**Max Tokens** [Concise <---> Detailed]", min_value=0,
                                max_value=4096, value=3072, step=8)
        TEMPERATURE = st.slider("**Temperature** [Factual <---> Creative]", min_value=0.0,
                                max_value=1.0, value=0.1, step=0.1)
        TOP_P = st.slider("**Top-P** [Focused <---> Diverse]", min_value=0.0,
                            max_value=1.0, value=0.5, step=0.01)

col1, col2 = st.columns([.45,.55])

with col1:
    # File uploader for PDFs
    uploaded_files = st.file_uploader("**Upload PDF files for context:**", type="pdf", accept_multiple_files=True)

with col2:
    # System Prompt
    system_prompt_selection = st.radio("**Choose a system prompt template:**", system_prompt_options, horizontal=True)
    system_prompt = system_prompt_options_dict[system_prompt_selection]
    system_prompt = st.text_area(
        "Prompt",
        height=120,
        value=system_prompt,
        label_visibility="collapsed"
    )

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
user_prompt_selection = st.radio("**Choose a user prompt template:**", user_prompt_options, horizontal=True)
user_prompt = user_prompt_options_dict[user_prompt_selection]
user_prompt = st.text_area(
    "Prompt",
    height=200,
    value=user_prompt,
    label_visibility="collapsed"
)

gen_button = st.button("Generate", type="primary")


# Button to generate content
if gen_button:
    # Prepare the conversation with PDF context
    conversation = [
        {
            "role": "user",
            "content": [{"text": f"{system_prompt}\n{user_prompt}\nHere is some context from uploaded PDF files:\n\n{combined_pdf_text}"}],
        }
    ]

    st.write("**GENERATED BY:** "+selected_model)
    st.write("**PARAMS:** Max Tokens ("+str(MAX_TOKENS)+") Temp ("+str(TEMPERATURE)+") Top-P ("+str(TOP_P)+")")

    timezone_offset = -4.0  # Eastern Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    start = datetime.now(tzinfo)

    try:
        with st.spinner("Generating response..."):
            # Send the message to the model
            response = client.converse(
                modelId=selected_model,
                messages=conversation,
                inferenceConfig={"maxTokens": MAX_TOKENS, "temperature": TEMPERATURE, "topP": TOP_P},
                # additionalModelRequestFields={"top_k": TOP_K} # NOT ALL MODELS SUPPORT TOP_K
            )

            end = datetime.now(tzinfo)
            st.write("**TIME TO GENERATE** = " + str(end - start))
            # Extract and display the response text
            response_text = response["output"]["message"]["content"][0]["text"]
            st.write("**Response:**")
            st.write(response_text)

    except ClientError as e:
        st.error(f"ClientError: Can't invoke '{selected_model}'. Reason: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
