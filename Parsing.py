from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from State import State
import LLM

file_paths = []   #put here the pdf file paths that you want to extract data from


def load_data(paths : list[str]) :
    """
    Load data from a list of paths.
    """
    data = []
    for path in paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
        data.extend(docs)
    return data
def split_data(documents ) :
    """
    Split data into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "."],  # tries paragraph, then line, then sentence
    )
    docs = text_splitter.split_documents(documents)
    return docs
def embed_data(documents ) -> FAISS:
    """
    Embed data into a vector store.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embedding_dim = len(embeddings.embed_query("hello world"))
    index = faiss.IndexFlatL2(embedding_dim)
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    _ = vector_store.add_documents(documents=documents)
    return vector_store

def create_vector_store():
    """
    Create a vector store from the data.
    
    Returns:
        vector_store: The vector store object.
    """
    documents = load_data(file_paths)
    docs = split_data(documents)
    return embed_data(docs)

def retrieve(state: State,vector_store):
    """Retrieve documents from the vector store based on the question."""
    retrieved_docs = vector_store.similarity_search(state["question"],k=3)
    return {"context": retrieved_docs}

def retrieve_modified(state: State, vector_store, llm ):
    """Retrieve documents from the vector store based on the question."""
    questions = LLM.rewrite_question(state["question"], llm)
    retrieved_docs = vector_store.similarity_search(state["question"],k=2)
    num_questions = 0
    for question in questions: 
        num_questions+=1
        if num_questions <=2:
            retrieved_docs.extend(vector_store.similarity_search(question, k=2 ))
    return {"context": retrieved_docs}

