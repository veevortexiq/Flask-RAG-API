from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
#retrieving vector store
from app.utils.vector_store import get_vectorstore
#storing retreival Chain
from app.utils.chain_store import init_chain
def setuplangchain():
    print("setting up langchain")
    llm = ChatOpenAI(openai_api_key="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",model_name="gpt-3.5-turbo", temperature=0)
    prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an assistant for answering questions based on retrieved information.

When a user asks a question, match the query with the correct tool and extract and respond with the tool name, required parameters, and agent ID in JSON format.

Use the following context to answer the question:

- Provide only the tool name, the "responses" column (required parameters), and the agent ID as an output in JSON format.
- The "required parameter" should be an array.
- Step-by-step reasoning is required before providing the final answer:
  1. First, analyze and break down the context into logical steps.
  2. Then, provide a structured and reasoned explanation for how you arrived at the final answer.

After completing your reasoning steps, provide only the tool name, required parameter, agent ID and Endpoint as a JSON object under the keys `"tool_name"`, `"req_param"`,`"agent_id"` and `"endpoint"`. If no relevant response is found, return `null` for all keys.
Context: {context}
Question: {question}

Answer:"""
)
    vectorstore=get_vectorstore()
    retrieval_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    combine_docs_chain_kwargs={"prompt": prompt_template},
    return_source_documents=True 
)
    init_chain(retrieval_chain)