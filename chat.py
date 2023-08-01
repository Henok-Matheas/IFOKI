import os
from dotenv import load_dotenv
import openai
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from cachetools import TTLCache, cached


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
CACHE_SIZE, CACHE_TIME = int(os.getenv("CACHE_SIZE")), int(os.getenv("CACHE_TIME"))

current_dir = os.path.dirname(__file__)
cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TIME)

@cached(cache)
def load_instruction(filename):
    f = open(filename, encoding='utf-8')
    return f.read()

@cached(cache)
def load_chat(address):
    chat = chat = ChatOpenAI(model='gpt-3.5-turbo-16k', temperature=0)
    instructions_file = os.path.join(current_dir,'CHATBOT_INSTRUCTIONS.txt')
    instructions = load_instruction(instructions_file)
    system_message_prompt = SystemMessagePromptTemplate.from_template(instructions)

    system_message_prompt.format_messages()
    human_template = """
    Your responses should not be more than 100 words. Since people don't want to read more than that. Keep your responses informative and to the point.
    If asked for more elaboration, you can write more. But try to keep it short and simple.
    input = {input}
    """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        MessagesPlaceholder(variable_name="history"),
        human_message_prompt
    ])

    memory = ConversationBufferMemory(input_key = "input", output_key="response", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=chat_prompt, llm=chat)
    return conversation