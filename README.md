# Custom-RAG-system


This project is a RAG system that uses LangChain and Streamlit.

I used the LangChain library to create a graph that processes a question and returns a response.
I used the Streamlit library to create a web interface for the RAG system.

The RAG system is a simple system that takes a question as input and returns a response.

The system is split into 4 files:
- main.py: the main file that runs the RAG system on the console.
- interface.py: the file that creates the web interface for the RAG system.
- Request.py: the file that contains the functions that process the question and return the response.
- Parsing.py: the file that contains the functions that read the pdf files and return the index file and the vector store.
- LLM.py: the file that contains the functions that generate the response.
- Create_index.py : The file that creates the index folder

The chat model used is mistral_large. 

To run tha rag an API key for mistral is required. The key can either be a environment variable or a parameter in the function call.

The mode can be set to 1 or 2. 
1 is the default and simple mode and uses similarity search to find the context that corresponds the most to the question. 
2 uses the modified method to retrieve documents. The modified method is more costly in terms of tokens , the model generates additional questions that can help provide additional
and more relevant context to the question. 

The Interface.bat file executes the streamlit interface directly


You need to insert the file paths manually in the file Parsing.py  , the files treated are in pdf format and the system works ideally with a small number of files


T
