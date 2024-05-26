import os
import streamlit as st
import replicate
from prompt_templates import title_template, script_template, memoryT, memoryS

# Set up Streamlit page configuration
st.set_page_config(page_title="DigiChat: An LLM Powered Chat")

# Function to generate YouTube link based on a text prompt currently points to the resources keeping ethical aspects in consideration
def generate_youtube_link(prompt_text):
    youtube_link = f"https://www.youtube.com/results?search_query={prompt_text.replace(' ', '+')}"
    return youtube_link

# Function to generate LLaMA2 response
def generate_llama2_response(prompt_input, model, temperature, top_p, max_length):
    dialogue_history = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\n"
    for message in st.session_state.messages[1:]:  # Skip the initial assistant message
        if message["role"] == "user":
            dialogue_history += f"User: {message['content']}\n\n"
        else:
            dialogue_history += f"Assistant: {message['content']}\n\n"

    response = replicate.run(
        model,
        input={
            "prompt": f"{dialogue_history}{prompt_input} Assistant: ",
            "temperature": temperature,
            "top_p": top_p,
            "max_length": max_length,
            "repetition_penalty": 1
        }
    )
    return response

# Clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi there, how may I assist you today?"}]

# Sidebar contents
with st.sidebar:
    st.title('DigiChat: An LLM Powered Chatbot')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')

    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if replicate_api.startswith('r8_') and len(replicate_api) == 40:
            st.success('Proceed to entering your prompt message!', icon='👉')
        else:
            st.warning('Please enter your credentials!', icon='⚠️')

    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        model_ref = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        model_ref = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.slider('Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.slider('Top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=32, max_value=128, value=120, step=8)
    st.markdown("References: https://www.geeksforgeeks.org/build-chatbot-webapp-with-langchain/, https://www.youtube.com/watch?v=J8TgKxomS2g")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there, how may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history button
if st.sidebar.button('Clear Chat History'):
    clear_chat_history()

# User-provided prompt
prompt_input = st.chat_input(disabled=not replicate_api, placeholder="Type here...")

# Generate a new response if last message is not from assistant
if prompt_input:
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.spinner("Thinking..."):
        if "YouTube title about" in prompt_input:
            concept = prompt_input.split("YouTube title about ")[-1]
            title = title_template.format(concept=concept)
            st.session_state.messages.append({"role": "assistant", "content": title})
        elif "Explain" in prompt_input:
            title = prompt_input.split("Explain ")[-1]
            wikipedia_research = "Wikipedia research goes here."  # Placeholder for Wikipedia research data
            script = script_template.format(title=title, wikipedia_research=wikipedia_research)
            st.session_state.messages.append({"role": "assistant", "content": script})
        else:
            response = generate_llama2_response(prompt_input, model_ref, temperature, top_p, max_length)
            response_text = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Generate a YouTube link if specified in the prompt
        if "YouTube link" in prompt_input:
            youtube_link = generate_youtube_link(prompt_input)
            st.session_state.messages.append({"role": "assistant", "content": youtube_link})

# Display updated chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])






