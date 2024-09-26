import streamlit as st

pg = st.navigation([
    st.Page("Home.py", title="Home", icon="🏠"), 
    st.Page("pages/Product_Review_Summarizer.py", title="Product_Review_Summarizer", icon="📖"), 
    st.Page("pages/Product_Blog_Writer.py", title="Product_Blog_Writer", icon="📝"), 
    st.Page("pages/Product_Content_Generator.py", title="Product_Content_Generator", icon="⚙️"), 
    st.Page("pages/Document_FAQ_Generator.py", title="Document_FAQ_Generator", icon="⁉️")
    # st.Page("pages/Product_Assistant_Chat.py", title="Product_Assistant_Chat", icon="💬")
])

pg.run()
