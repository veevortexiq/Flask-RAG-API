from langchain.chains import ConversationalRetrievalChain

retrieval_chain = None

def init_chain(new_chain):
    global retrieval_chain
    retrieval_chain = new_chain

def get_chain():
    return retrieval_chain