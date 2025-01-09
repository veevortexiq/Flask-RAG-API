from langchain.vectorstores import FAISS

# Global variable to store the vectorstore
vectorstore = None

def init_vectorstore(new_vectorstore):
    global vectorstore
    vectorstore = new_vectorstore

def get_vectorstore():
    return vectorstore