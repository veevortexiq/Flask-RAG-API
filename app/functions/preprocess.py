from dotenv import load_dotenv
import os
import pandas as pd
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
#saving VectorStore
from app.utils.vector_store import init_vectorstore
def preprocess_csv() :
    load_dotenv()
    print("Preprocess starting")
    # Load dataset (replace with your dataset path)
    dataset_path = r"app\data\updated_csv.csv"
    data = pd.read_csv(dataset_path)
    # Combine relevant columns into a single context field
    data['context'] = data['Passages'] + " " + data['Meta Data'] + " " + data['Query'] + " , Tool Name: " + data['Tool Name']+ " , Required Parameters :  " + data['Responses']+ " , Agent ID :  " + (data['Agent Id'].astype(str)) + " , Endpoint:  " + (data['endpoints'].astype(str))
    # Handle missing values by replacing NaN with an empty string
    data['context'] = data['context'].fillna("")
    # Load SBERT model
    sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    # Generate embeddings for each row in the context column
    embeddings = sbert_model.encode(data['context'].tolist(), convert_to_tensor=False)
    # Create a FAISS vector store with the embeddings and corresponding metadata
    documents = [Document(page_content=row['context'], metadata={"query": row["Query"], "response": row["Responses"]})for _, row in data.iterrows()]
    vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY')))
    init_vectorstore(vectorstore)