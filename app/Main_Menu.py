import streamlit as st

pg = st.navigation({"Main Menu" : [
    st.Page("Home.py", title="Home", icon="🏠"), 
    st.Page("demos/Product_Content_Generator.py", title="Product_Content_Generator", icon="✍️"),
    st.Page("demos/Product_Image_Reader.py", title="Product_Image_Reader", icon="📸"), 
    st.Page("demos/Product_Review_Summarizer.py", title="Product_Review_Summarizer", icon="📖"), 
    st.Page("demos/Product_Assistant_Chat.py", title="Product_Assistant_chat", icon="💬")
]})

pg.run()
