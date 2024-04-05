import streamlit as st
from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat
from langchain.prompts import PromptTemplate


def get_inference_parameters(model_id, temperature): #return a default set of parameters based on the model's provider
    bedrock_model_provider = model_id.split('.')[0] #grab the model provider from the first part of the model id
    
    if (bedrock_model_provider == 'anthropic'): #Anthropic model
        return { #anthropic
            "max_tokens": 4000,
            "temperature": temperature, 
            "top_k": 250, 
            "top_p": 1, 
            "stop_sequences": ["\n\nHuman:"] 
           }
    
    elif (bedrock_model_provider == 'ai21'): #AI21
        return { #AI21
            "maxTokens": 4000, 
            "temperature": temperature, 
            "topP": 0.5, 
            "stopSequences": [], 
            "countPenalty": {"scale": 0 }, 
            "presencePenalty": {"scale": 0 }, 
            "frequencyPenalty": {"scale": 0 } 
           }
    
    elif (bedrock_model_provider == 'cohere'): #COHERE
        return {
            "max_tokens": 4000,
            "temperature": temperature,
            "p": 0.5,
            "k": 0,
            "stop_sequences": [],
            "return_likelihoods": "NONE"
        }
    
    elif (bedrock_model_provider == 'meta'): #META
        return {
            "temperature": temperature,
            "top_p": 0.9,
            "max_gen_len": 2000 #temp
        }
    
    elif (bedrock_model_provider == 'mistral'): #MISTRAL
        return {
            "max_tokens" : 4000,
            "stop" : [],    
            "temperature": 0,
            "top_p": 0.9,
            "top_k": 50
        }
    
    else: #Amazon
        #For the LangChain Bedrock implementation, these parameters will be added to the 
        #textGenerationConfig item that LangChain creates for us
        return { 
            "maxTokenCount": 4000, 
            "stopSequences": [], 
            "temperature": temperature, 
            "topP": 0.9 
        }


def get_llm(model_id, temperature):
    
    model_kwargs = get_inference_parameters(model_id, temperature)
    
    bedrock_model_provider = model_id.split('.')[0] #grab the model provider from the first part of the model id
    
    if bedrock_model_provider == 'anthropic' or bedrock_model_provider == 'mistral' or bedrock_model_provider == 'meta' or bedrock_model_provider == 'amazon':
        llm = BedrockChat(
            model_id=model_id, #set the foundation model
            model_kwargs=model_kwargs) #configure the properties for the LLM
        
        is_chat = True
    else:
        llm = Bedrock(
            model_id=model_id, #set the foundation model
            model_kwargs=model_kwargs) #configure the properties for the LLM
        
        is_chat = False
    return llm, is_chat


def read_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()
     
    return text


def get_context_list():
    return ["Insulation Reviews", "Blank"]
    

def get_context(lab):
    if lab == "Insulation Reviews":
        return read_file("/home/ubuntu/environment/amazon-bedrock-genai-streamlit/app/pages/data/insulation-reviews.txt")
    elif lab == "Blank":
        return ""


def get_prompt(template, context=None, user_input=None):
    
    prompt_template = PromptTemplate.from_template(template) #this will automatically identify the input variables for the template
    
    if "{context}" not in template:
        prompt = prompt_template.format()
    else:
        prompt = prompt_template.format(context=context) #, user_input=user_input)
    
    return prompt



def get_text_response(model_id, temperature, template, context=None, user_input=None): #text-to-text client function
    llm, is_chat = get_llm(model_id, temperature)
    
    prompt = get_prompt(template, context, user_input)
    
    response = llm.invoke(prompt) #return a response to the prompt
    
    if is_chat:
        response = response.content
    
    # print(response)
    
    return response


model_options_dict = {
    "anthropic.claude-3-sonnet-20240229-v1:0": "Claude 3 Sonnet",
    "anthropic.claude-3-haiku-20240307-v1:0" : "Claude 3 Haiku",
    "mistral.mixtral-8x7b-instruct-v0:1": "Mixtral 8x7b Instruct",
    "mistral.mistral-large-2402-v1:0" : "Mixtral Large",
    "meta.llama2-70b-chat-v1": "Llama 2 70b Chat",
    "ai21.j2-ultra-v1": "Jurassic 2 Ultra",
    "cohere.command-text-v14": "Command",
    "amazon.titan-text-express-v1": "Titan Text Express"
}

model_options = list(model_options_dict)

def get_model_label(model_id):
    return model_options_dict[model_id]
    
st.set_page_config(page_title="Summarize Product Reviews", layout="wide", page_icon="📖")
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
        format_func=get_model_label,
        horizontal=True
        #label_visibility="collapsed"
    )
    
    #selected_temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    
    process_button = st.button("Generate", type="primary")

if process_button:
    with st.spinner("Generating..."):
        response_content = get_text_response(model_id=selected_model, temperature=0.0, template=prompt_text, context=context_text)
        st.subheader("Results")
        st.write(response_content)
