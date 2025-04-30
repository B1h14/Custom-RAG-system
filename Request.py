import Parsing
import LLM
from State import State
from langgraph.graph import START, StateGraph
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

MODE = 1
API_KEY = None

def set_graph(llm,vector_store):
    """Set up a graph for processing a question.
    
    Args:
        llm: The language model to use for processing.
        vector_store: The vector store to use for document retrieval.
    
    Returns:
        graph: The graph object.
    """
    def retrieve(state):
        return Parsing.retrieve(state,vector_store)
    def generate(state):
        return LLM.generate(state,llm)
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph
def set_graph_modified(llm,vector_store):
    """Set up a graph for processing a question.
    
    Args:
        llm: The language model to use for processing.
        vector_store: The vector store to use for document retrieval.
    
    Returns:
        graph: The graph object.
    """
    def retrieve(state):
        return Parsing.retrieve_modified(state,vector_store, llm)
    def generate(state):
        return LLM.generate(state,llm)
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    return graph
def get_response(graph,request):
    """Get a response from the graph.
    
    Args:
        graph: The graph object.
        request: The request to process.
    
    Returns:
        response: The response from the graph.
    """
    response = graph.invoke({"question": request})
    return response["answer"]

def set_up(API_KEY= None,mode = 1):
    if API_KEY:
        llm = LLM.get_llm(API_KEY)
    else :
        llm = LLM.get_llm()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local("index", embeddings,allow_dangerous_deserialization=True)
    if mode == 1:
        graph = set_graph(llm, vector_store)
        return graph
    elif mode == 2:
        return set_graph_modified(llm, vector_store)
    else:
        raise ValueError("Invalid mode")
