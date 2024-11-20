
import streamlit as st

st.set_page_config(page_title="AWS Generative AI Demos", page_icon="🏠", layout="wide")

st.write("### Generative AI Demos")
st.caption("A collection of Digital Marketing focused generative AI demos built on Amazon Bedrock.")
""

col1, col2 = st.columns([.5,.5], gap="large")

with col1:
    st.page_link("demos/Product_Content_Generator.py", icon="❓", label="**Product Content Generator**")
    "Use PDF documents to generate product descriptions, FAQs, metadata, blog posts, social media posts, feature lists, amd more..."
    ""

    st.page_link("demos/Product_Image_Reader.py", icon="📸", label="**Product Image Reader**")
    "Use product images to generate product descriptions, feature lists, and meta tag code for Open Graph, schema.org, and more..."
    ""

with col2:
    st.page_link("demos/Product_Review_Summarizer.py", icon="📖️", label="**Product Review Summarizer**")
    "List the most common positive and negative comments from a set of consumer product reviews and summarize the overall sentiment."
    ""
    
    st.page_link("demos/Product_Assistant_chat.py", icon="💬", label="**Product Assistant Chatbot**")
    "Have a conversation with a Claude 3 chatbot."
    ""
