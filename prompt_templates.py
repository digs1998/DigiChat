from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Setting up the prompt templates

title_template = PromptTemplate(
    input_variables=['concept'],
    template='Give me a youtube video title about {concept}'
)

script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='''Explain {title} to me as an absolute beginner 
    while making use of the information and knowledge obtained from the Wikipedia research:{wikipedia_research}'''
)

# Conversation buffer memory
memoryT = ConversationBufferMemory(input_key='concept', memory_key='chat_history')
memoryS = ConversationBufferMemory(input_key='title', memory_key='chat_history')
