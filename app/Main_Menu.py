import streamlit as st

pg = st.navigation({"Main Menu" : [
    st.Page("Home.py", title="Home", icon="🏠"), 
    st.Page("demos/Product_FAQ_Generator.py", title="Product_FAQ_Generator", icon="❓"),
    st.Page("demos/Product_Metadata_Generator.py", title="Product_Metadata_Generator", icon="🛠️"),
    st.Page("demos/Product_Image_Reader.py", title="Product_Image_Reader", icon="📷"), 
    st.Page("demos/Product_Review_Summarizer.py", title="Product_Review_Summarizer", icon="📖"), 
    st.Page("demos/Product_Blog_Writer.py", title="Product_Blog_Writer", icon="📝"), 
    # st.Page("demos/Document_FAQ_Generator.py", title="Document_FAQ_Generator", icon="⁉️"),
    st.Page("demos/Product_Assistant_Chat.py", title="Product_Assistant_Chat", icon="💬")
]})

pg.run()
