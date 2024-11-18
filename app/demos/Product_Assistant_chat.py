# ------------------------------------------------------
# Streamlit
# Knowledge Bases for Amazon Bedrock and LangChain 🦜️🔗
# ------------------------------------------------------

import boto3
import logging

from typing import List, Dict
from pydantic import BaseModel
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_aws import ChatBedrock
from langchain_aws import AmazonKnowledgeBasesRetriever
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# ------------------------------------------------------
# Log level

logging.getLogger().setLevel(logging.ERROR) # reduce log level


def get_all_kbs(all_kb: dict) -> dict[str, str]:
    """
    Extract knowledge base names and IDs from the response.

    Args:
        all_kb (dict): The response from the list_knowledge_bases API call.

    Returns:
        Dict[str, str]: A dictionary mapping knowledge base names to their IDs.
    """
    result = {}
    for kb in all_kb["knowledgeBaseSummaries"]:
        result[kb["name"]] = kb["knowledgeBaseId"]
    return result

# ------------------------------------------------------
# Streamlit

import streamlit as st

# Page title
#st.set_page_config(page_title='Knowledge Bases for Amazon Bedrock and LangChain 🦜️🔗')

INIT_MESSAGE = {
    "role": "assistant",
    "content": "Hi! I'm Claude 3 on Bedrock. How can I help you today?"
}

SYSTEM_PROMPT_MSG = """You are a friendly, professional chatbot."""

model_map = {
    "Sonnet": "us.anthropic.claude-3-sonnet-20240229-v1:0",
    "Haiku": "us.anthropic.claude-3-haiku-20240307-v1:0"
}

bedrock_agents_client = boto3.client(
    service_name="bedrock-agent", region_name="us-east-1",
)

all_kbs = get_all_kbs(bedrock_agents_client.list_knowledge_bases(maxResults=10))

# Sidebar info
with st.sidebar:
    st.markdown("## LLM Parameters")
    SYSTEM_PROMPT = st.text_area("**Context**",SYSTEM_PROMPT_MSG, height=100)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            MODEL_NAME = st.selectbox('**Claude 3 Model**', ('Sonnet', 'Haiku'))
            MODEL_ID = model_map.get(MODEL_NAME)
        with col2:
            KB_SELECTION = st.selectbox(
                "**Bedrock KB**", ["None"] + list(all_kbs.keys()), index=0
            )

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            TOP_P = st.slider("**Top-P**", min_value=0.0,
                              max_value=1.0, value=1.0, step=0.01)
        with col2:
            TOP_K = st.slider("**Top-K**", min_value=1,
                      max_value=500, value=250, step=5)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            MAX_TOKENS = st.slider("**Max Tokens**", min_value=0,
                                   max_value=4096, value=2048, step=8)
        with col2:
            TEMPERATURE = st.slider("**Temperature**", min_value=0.0,
                                    max_value=1.0, value=0.1, step=0.1)
            # MEMORY_WINDOW = st.slider("**Memory Window**", min_value=0,
            #                           max_value=10, value=10, step=1)

SELECTED_KB_ID = (
    all_kbs[KB_SELECTION]
    if KB_SELECTION != "None"
    else "ADSTTXVI4L"
)

st.title("🤖 Product Assistant Chatbot")
st.caption("Model: " + MODEL_ID + "  |  KB: " + KB_SELECTION)

# ------------------------------------------------------
# Amazon Bedrock - settings

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

model_kwargs = {'temperature': TEMPERATURE,
                'top_p': TOP_P,
                'top_k': TOP_K,
                'max_tokens': MAX_TOKENS,
                'stop_sequences': ["\n\nHuman"],
                'system': SYSTEM_PROMPT}

# ------------------------------------------------------
# LangChain - RAG chain with chat history

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a friendly, professional chatbot."
         "Answer the question based only on the following context:\n {context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Amazon Bedrock - KnowledgeBase Retriever 
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=SELECTED_KB_ID, # 👈 Set your Knowledge base ID
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 3}},
)

model = ChatBedrock(
    client=bedrock_runtime,
    model_id=MODEL_ID,
    model_kwargs=model_kwargs,
)

chain = (
    RunnableParallel({
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "history": itemgetter("history"),
    })
    .assign(response = prompt | model | StrOutputParser())
    .pick(["response", "context"])
)

# Streamlit Chat Message History
history = StreamlitChatMessageHistory(key="chat_messages")

# Chain with History
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    input_messages_key="question",
    history_messages_key="history",
    output_messages_key="response",
)

# ------------------------------------------------------
# Pydantic data model and helper function for Citations

class Citation(BaseModel):
    page_content: str
    metadata: Dict

def extract_citations(response: List[Dict]) -> List[Citation]:
    return [Citation(page_content=doc.page_content, metadata=doc.metadata) for doc in response]

# ------------------------------------------------------
# S3 Presigned URL

def create_presigned_url(bucket_name: str, object_name: str, expiration: int = 300) -> str:
    """Generate a presigned URL to share an S3 object"""
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        st.error("AWS credentials not available")
        return ""
    return response

def parse_s3_uri(uri: str) -> tuple:
    """Parse S3 URI to extract bucket and key"""
    parts = uri.replace("s3://", "").split("/")
    bucket = parts[0]
    key = "/".join(parts[1:])
    return bucket, key


# Clear Chat History function
def clear_chat_history():
    history.clear()
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    st.button('Clear Chat History', on_click=clear_chat_history)
    st.divider()
    st.write("History Logs")
    st.write(history.messages)

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat Input - User Prompt 
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    config = {"configurable": {"session_id": "any"}}
    
    # Chain - Stream
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ''
        for chunk in chain_with_history.stream(
            {"question" : prompt, "history" : history},
            config
        ):
            if 'response' in chunk:
                full_response += chunk['response']
                placeholder.markdown(full_response)
            else:
                full_context = chunk['context']
        placeholder.markdown(full_response)
        # Citations with S3 pre-signed URL
        citations = extract_citations(full_context)
        with st.expander("Show source details >"):
            for citation in citations:
                st.write("Page Content:", citation.page_content)
                # st.write("Metadata:", citation.metadata)

                if citation.metadata['location']['type'] == "WEB":
                    st.write("URL:", citation.metadata['location']['webLocation']['url'])

                # if citation.metadata['location']:
                #     s3_uri = citation.metadata['location']['s3Location']['uri']
                #     bucket, key = parse_s3_uri(s3_uri)
                #     presigned_url = create_presigned_url(bucket, key)
                #     if presigned_url:
                #         st.markdown(f"Source: [{s3_uri}]({presigned_url})")
                #     else:
                #         st.write(f"Source: {s3_uri} (Presigned URL generation failed)")
                st.write("Score:", citation.metadata['score'])
                st.divider()

        # session_state append
        st.session_state.messages.append({"role": "assistant", "content": full_response})

