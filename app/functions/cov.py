
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.functions.initial_query import initalquery
from app.utils.chain_store import get_chain

def execute_verifications(questions, baseline_response,documents):
    load_dotenv()
    verification_template = PromptTemplate(
        input_variables=["question", "api_endpoint", "payload_template"],
        template=
        """question: {question}
        documents: {documents},
       baseline_response : {baseline_response}
        be more stringent in verification.
        Verify and provide a breif response. If the tool doesn't match, recommend in the answer to choose a different tool"""
    )

    llm = ChatOpenAI(temperature=0.3,openai_api_key=os.getenv('OPENAI_API_KEY'))
    chain = LLMChain(llm=llm, prompt=verification_template)

    verification_results = []
    for question in questions:
        result = chain.run({
            'question': question,
            'baseline_response': baseline_response,
            'documents' : documents
        })


        verification_results.append(result)

    return verification_results


from langchain.chains import LLMChain

def generate_final_response(baseline_response, verification_results,relevant_documents):
    load_dotenv()
    final_template = PromptTemplate(
        input_variables=["baseline_response", "verification_results", "relevant_documents"],
        template="""Initial Response: {baseline_response}
        Verification Results: {verification_results}
        relevant Documents {relevant_documents}
        Generate a final, verified response with high confidence.After completing your reasoning steps, provide only the tool name, required parameter, agent ID and Endpoint as a JSON object under the keys `"tool_name"`, `"req_param"`, and `"agent_id"`. If no relevant response is found, return `null` for all keys,
        if the /Cove failes just reponse with "null" nothing else. make sure it outputs a valid json. If tool name is null in the baseline response, chack the question is relevant or not, if it's not, return null"""
    )

    llm = ChatOpenAI(temperature=0.0,openai_api_key=os.getenv('OPENAI_API_KEY'))
    chain = LLMChain(llm=llm, prompt=final_template)

    final_response = chain.run({
        'baseline_response': str(baseline_response),
        'verification_results': str(verification_results),
        'relevant_documents': str(relevant_documents)
    })

    return final_response


def process_query(user_query):
    # Step 1: Generate baseline response
    # print("started execution of init query")
    baseline = initalquery(user_query, get_chain())
    # print("baseline-->",baseline)
    # print("ended execution of init query")
    verification_questions = ["Does the Question matches with the kind of tool user asked?","Does the Baseline response has all the required parameter it needs?","Does the response has toolname, responses,agent_id mapped correctly"]
    # Step 3: Execute verifications
    # print("started execution of verificatoin")

    verification_res = execute_verifications(verification_questions,baseline[0],baseline[1])
    # print("veri res", verification_res)
    
    # print("ended execution of verificatoin")
    
    # print("\nVerification Results:", verification_res)
    # print("started execution of FINAL Verification")
    # Step 4: Generate final response
    final_response = generate_final_response(baseline[0],verification_res,baseline[1])
    # print("ended execution of FINAL Verification")

    return final_response