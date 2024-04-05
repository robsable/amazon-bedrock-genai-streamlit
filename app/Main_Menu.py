import streamlit as st

st.set_page_config(
    page_title="AWS Gen AI Demos",
    page_icon="👋",
    layout="wide", 
)

st.write("# AWS Generative AI Demos")

st.sidebar.success("☝️Select a demo above.")

"""👈 *Choose a demo from the main menu*

---"""

st.page_link("pages/1_Product_Content_Generator.py", 
    icon="⚙️", label="**Product Metadata Generator**")
"Use product images to generate product descriptions, feature lists, and meta tag code for Open Graph, schema.org, and more..."
"---"

st.page_link("pages/2_Product_Review_Summarizer.py", 
    icon="📖️", label="**Product Review Summarizer**")
"List the most common positive and negative comments from a set of consumer product reviews and summarize the overall sentiment."
"---"

st.page_link("pages/3_Product_Blog_Writer.py", 
    icon="📝️", label="**Product Blog Writer**")
"Generate a 750-1000 word blog post with a comma-separated list of related SEO keywords."
"---"

# st.markdown(
# """
# ---
# ###### ⁉️ Product FAQ Generator
# Use product documentation to generate a list of expected customer questions and their answers.

# ---
# ###### 💬 Claude 3 Bedrock Chatbot
# Have a text and image-based conversation with a Claude 3 chatbot.

# ---
# ###### 💬 Claude 2.1 Bedrock Chatbot
# Have a conversation with a Claude 2.1 chatbot.
# """
# )