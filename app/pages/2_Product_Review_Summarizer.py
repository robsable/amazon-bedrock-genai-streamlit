import streamlit as st
from langchain.prompts import PromptTemplate
from pathlib import Path
from datetime import datetime, timezone, timedelta
from pages.lib import models_shared

def read_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()     
    return text

def get_context_list():
    return ["Insulation Reviews", "Blank"]  

def get_context(lab):
    base_path = Path(__file__).parent

    if lab == "Insulation Reviews":
        return read_file(base_path / "data/insulation-reviews.txt")
    elif lab == "Blank":
        return ""

def get_prompt(template, context=None, user_input=None):
    
    prompt_template = PromptTemplate.from_template(template) #this will automatically identify the input variables for the template
    
    if "{context}" not in template:
        prompt = prompt_template.format()
    else:
        prompt = prompt_template.format(context=context) 
    
    return prompt

def get_text_response(model_id, temperature, template, context=None, user_input=None): #text-to-text client function
    llm, is_chat = models_shared.get_llm(model_id, temperature)
    
    prompt = get_prompt(template, context, user_input)
    
    response = llm.invoke(prompt) #return a response to the prompt
    
    if is_chat:
        response = response.content
    
    return response

#################
# Streamlit App #
#################

# Get Bedrock LLM Models options
model_options = list(models_shared.model_options_dict)

st.set_page_config(page_title="Summarize Product Reviews", layout="wide", page_icon=":open_book:")
st.title("Summarize Product Reviews")
st.caption("**Instructions:**  (1) Select a context (2) Click Show context to see reviews data (3) Customize prompt text as needed (4) Select a model  (5) Click Generate")

col1, col2 = st.columns([.25,.75])

with col1:
    context_list = get_context_list()
    
    selected_context = st.radio(
        "**Select a context:**",
        context_list,
        #label_visibility="collapsed"
    )
    
    with st.expander("Show context"):
        context_for_lab = get_context(selected_context)
        context_text = st.text_area("**Enter context text:**", value=context_for_lab, height=200)

with col2:
    prompt_text = st.text_area("**Enter prompt text:**", value="{context}\r\n\r\nList the most common positive and negative comments.  What is the overall sentiment?", height=150)
    
    selected_model = st.radio("**Select a model:**", 
        model_options,
        format_func=models_shared.get_model_label,
        horizontal=True
    )
    
    process_button = st.button("Generate", type="primary")

if process_button:
    with st.spinner("Generating..."):

        timezone_offset = -4.0  # Eastern Standard Time (UTC−08:00)
        tzinfo = timezone(timedelta(hours=timezone_offset))

        start = datetime.now(tzinfo)

        response_content = get_text_response(model_id=selected_model, temperature=0.0, template=prompt_text, context=context_text)

        end = datetime.now(tzinfo)
        
        st.subheader("Results")
        st.write("**TIME TO GENERATE** = " + str(end - start))
        st.write(response_content)
