
import streamlit as st

st.set_page_config(page_title="AWS Generative AI Demos", page_icon="🏠", layout="wide")

st.write("### Generative AI Demos")
st.caption(":rocket: A collection of Digital Marketing focused generative AI demos on Amazon Bedrock.")
""

col1, col2 = st.columns([.5,.5], gap="large")

with col1:
    st.page_link("pages/Product_Review_Summarizer.py", icon="📖️", label="**Product Review Summarizer**")
    "List the most common positive and negative comments from a set of consumer product reviews and summarize the overall sentiment."
    ""

    st.page_link("pages/Product_Content_Generator.py", icon="⚙️", label="**Product Content Generator**")
    "Use product images to generate product descriptions, feature lists, and meta tag code for Open Graph, schema.org, and more..."
    ""

with col2:
    st.page_link("pages/Product_Blog_Writer.py", icon="📝️", label="**Product Blog Writer**")
    "Generate a 750-1000 word blog post with a comma-separated list of related SEO keywords."
    ""

    st.page_link("pages/Document_FAQ_Generator.py", icon="⁉️", label="**Document FAQ Generator**")
    "Use PDF documents to generate a list of expected customer questions and their answers."

    # st.page_link("pages/Product_Assistant_Chat.py", icon="💬", label="**Product Assistant Chatbot**")
    #"Have a text and image-based conversation with a Claude 3 chatbot."
