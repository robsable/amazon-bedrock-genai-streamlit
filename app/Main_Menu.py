import streamlit as st
from st_pages import show_pages_from_config, add_indentation

st.set_page_config(page_title="AWS Generative AI Demos", page_icon=":house:", layout="wide")
add_indentation()
show_pages_from_config()

st.write("### AWS Generative AI Demos")
st.caption(":point_left: *Choose a demo from the main menu*")
""

col1, col2 = st.columns([.5,.5], gap="large")

with col1:
    st.page_link("pages/Product_Metadata_Generator.py", icon="⚙️", label="**Product Metadata Generator**")
    "Use product images to generate product descriptions, feature lists, and meta tag code for Open Graph, schema.org, and more..."
    ""

    st.page_link("pages/Product_Review_Summarizer.py", icon="📖️", label="**Product Review Summarizer**")
    "List the most common positive and negative comments from a set of consumer product reviews and summarize the overall sentiment."
    ""
    st.page_link("pages/Document_FAQ_Generator.py", icon="⁉️", label="**Document FAQ Generator**")
    "Use PDF documents to generate a list of expected customer questions and their answers."
    ""

with col2:
    st.page_link("pages/Product_Blog_Writer.py", icon="📝️", label="**Product Blog Writer**")
    "Generate a 750-1000 word blog post with a comma-separated list of related SEO keywords."
    ""

    st.page_link("pages/Claude_3_Chatbot.py", icon="💬", label="**Claude 3 Chatbot**")
    "Have a text and image-based conversation with a Claude 3 chatbot."
    ""
