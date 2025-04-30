import os
import getpass
from langchain.chat_models import init_chat_model
from State import State
from langchain import hub
prompt = hub.pull("rlm/rag-prompt")
from langchain.prompts import PromptTemplate

prompt_modifiy_question = PromptTemplate.from_template("""
You are an assistant designed to help you formulate a question to extract info.

When given a user input, you must:
- Analyze the question
- Think of two questions where the combined answers of each questions gives context to respond to the original question
- Provide these questions in this format :
<question1>;;;<question2>
- Respond only with the questions
Begin!

User Input: {question}
""")

def set_API_key():
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

def get_llm(API_KEY=None):
    if API_KEY:
        os.environ["MISTRAL_API_KEY"] = API_KEY
    else :
        set_API_key()
    llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
    return llm


def generate(state: State, llm ):
    """Generate a response from the language model.
    
    Args:
        state: The state object.
        llm: The language model to use for processing.
    
    Returns:
        response: The response from the language model.
    """
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

def rewrite_question(question,llm):
    """Provide two questions that improve the recieved context.
    
    Args:
        question: The question to analyse.
        llm: The language model to use for processing.
    
    Returns:
        response: A list of two questions.
    """
    message = prompt_modifiy_question.invoke({"question": question})
    response = llm.invoke(message)
    return response.content.split(';;;')
    
