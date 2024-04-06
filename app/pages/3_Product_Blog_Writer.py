import streamlit as st
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler


CLAUDE_PROMPT = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

INIT_MESSAGE = {"role": "assistant",
                "content": "Hi! I'm Claude 3 on Bedrock. What would you like me to write an article about? For example:\r\n\r\n &nbsp;&bull;&nbsp; Explain the business benefits of the AWS cloud.\r\n\r\n &nbsp;&bull;&nbsp; How can I decommission my data center?\r\n\r\n &nbsp;&bull;&nbsp; How do you identify cloud migration opportunities?"}

SYSTEM_PROMPT_MSG = """You are an Amazon Web Services (AWS) cloud expert with access to lots of data on AWS products. 
You are using a professional writing style to convey technical information simply. 
Use bold headings and lists to communicate your points clearly. 
Embed as many hyperlinks as possible in the article to resources you are citing. 
Each article you write should be 750 to 1000 words long. 
Include a comma-separated list of applicable SEO keywords below the article.
"""

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Set Streamlit page configuration
st.set_page_config(page_title="Write a blog post", layout="wide", page_icon="📝")

model_map = {
    "Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "Haiku": "anthropic.claude-3-haiku-20240307-v1:0"
}

# Sidebar info
with st.sidebar:
    st.markdown("## Inference Parameters")
    SYSTEM_PROMPT = st.text_area("**System Prompt**",SYSTEM_PROMPT_MSG, height=150)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            MODEL_NAME = st.selectbox('**Claude 3 Model**', ('Sonnet', 'Haiku'))
            MODEL_ID = model_map.get(MODEL_NAME)
        with col2:
            TEMPERATURE = st.slider("**Temperature**", min_value=0.0,
                                    max_value=1.0, value=1.0, step=0.1)


    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            TOP_P = st.slider("**Top-P**", min_value=0.0,
                              max_value=1.0, value=0.75, step=0.01)
        with col2:
            TOP_K = st.slider("**Top-K**", min_value=1,
                      max_value=500, value=250, step=5)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            MAX_TOKENS = st.slider("**Max Tokens**", min_value=0,
                                   max_value=4096, value=4096, step=8)
        with col2:
            MEMORY_WINDOW = st.slider("**Memory Window**", min_value=0,
                                      max_value=10, value=0, step=1)

st.title("Bedrock Claude 3 Blog Writer")
st.caption("Model: " + MODEL_ID)

# Initialize the ConversationChain
def init_conversationchain() -> ConversationChain:
    model_kwargs = {'temperature': TEMPERATURE,
                    'top_p': TOP_P,
                    'top_k': TOP_K,
                    'max_tokens': MAX_TOKENS,
                    'system': SYSTEM_PROMPT}

    llm = BedrockChat(
        model_id=MODEL_ID,
        model_kwargs=model_kwargs,
        streaming=True
    )

    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=ConversationBufferWindowMemory(
            k=MEMORY_WINDOW, ai_prefix="Assistant", chat_memory=StreamlitChatMessageHistory(), return_messages=True),
        prompt=CLAUDE_PROMPT
    )

    # Store LLM generated responses

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [INIT_MESSAGE]

    return conversation


def generate_response(conversation: ConversationChain, input_text: str) -> str:
    return conversation.run(input=input_text, callbacks=[StreamHandler(st.empty())])


# Re-initialize the chat
def new_chat() -> None:
    st.session_state["messages"] = [INIT_MESSAGE]
    st.session_state["langchain_messages"] = []
    conv_chain = init_conversationchain()


# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

# Initialize the chat
conv_chain = init_conversationchain()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User-provided prompt
prompt = st.chat_input()

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        # print(st.session_state.messages)
        response = generate_response(conv_chain, prompt)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
