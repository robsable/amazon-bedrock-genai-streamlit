#
# Shared Library of LLM/Bedrock functions used across Streamlit apps
#
from langchain_community.llms import Bedrock
from langchain_community.chat_models import BedrockChat

vision_model_options_dict = {
    "anthropic.claude-3-sonnet-20240229-v1:0": "Claude 3 Sonnet",
    "anthropic.claude-3-haiku-20240307-v1:0" : "Claude 3 Haiku"
}

def get_vision_model_label(model_id):
    return vision_model_options_dict[model_id]

model_options_dict = {
    "amazon.titan-text-express-v1": "Titan Text Express",
    "amazon.titan-text-lite-v1": "Titan Text Lite",
    "anthropic.claude-3-sonnet-20240229-v1:0": "Claude 3 Sonnet",
    "anthropic.claude-3-haiku-20240307-v1:0" : "Claude 3 Haiku",
    "ai21.j2-ultra-v1": "Jurassic-2 Ultra",
    "ai21.j2-mid-v1": "Jurassic-2 Mid",
    "cohere.command-text-v14": "Command",
    "cohere.command-light-text-v14": "Command Light",
    "meta.llama2-70b-chat-v1": "Llama 2 Chat 70B",
    "meta.llama2-13b-chat-v1": "Llama 2 Chat 13B",
    "mistral.mistral-7b-instruct-v0:2": "Mixtral 7B Instruct",
    "mistral.mixtral-8x7b-instruct-v0:1": "Mixtral 8X7B Instruct",
    "mistral.mistral-large-2402-v1:0" : "Mixtral Large"
}

def get_model_label(model_id):
    return model_options_dict[model_id]

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
            "maxTokens": 8000, 
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

