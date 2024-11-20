import streamlit as st

pg = st.navigation({"Main Menu" : [
    st.Page("Home.py", title="Home", icon="🏠"), 
    st.Page("demos/Product_Content_Generator.py", title="Product Content Generator", icon="✍️"),
    st.Page("demos/Product_Image_Reader.py", title="Product Image Reader", icon="📸"), 
    st.Page("demos/Product_Review_Summarizer.py", title="Product Review Summarizer", icon="📖"), 
    st.Page("demos/Product_Assistant_chat.py", title="Product Assistant Chat", icon="💬")
]})

pg.run()
