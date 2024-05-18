from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
import csv
import json
from langchain.schema import Document

# 1 - Get the data (WhatsApp messages and emails) 
# The data must be added into the Document object for the chain to accept
data = Document(page_content="""5/13/24, 9:54 PM
            Gmail - New project details
            Hamish Lewis <hamish.lewis810@gmail.com>
            New project details
            3 messages
            Hamish Lewis <hamish.lewis810@gmail.com>
            To: "sevyngreta@gmail.com" <sevyngreta@gmail.com>
            Mon, May 13, 2024 at 9:03 PM
            Hi Sevyn,
            Happy to be part of this project, please can you update me on the latest details.
            Thanks,
            Hamish.
            Sevyn Greta <sevyngreta@gmail.com>
            To: Hamish Lewis <hamish.lewis810@gmail.com>
            Mon, May 13, 2024 at 9:35 PM
            Hi Hamish,
            Details of the project:
            A mouse pad with a built in screen for the user to display desktop background like images.
            The project is currently in concept phase, and some mock up designs are needed, can you please contact Vasco and
            ask him for technical details and then generate some designs. Send them to Vasco and myself.
            Thanks,
            Hamish.
            [Quoted text hidden]
            Hamish Lewis <hamish.lewis810@gmail.com>
            To: Sevyn Greta <sevyngreta@gmail.com>
            Mon, May 13, 2024 at 9:36 PM
            Yes, no problem.
            [Quoted text hidden]
            https://mail.google.com/mail/u/5/?ik=33df3b7ed3&view=pt&search=all&permthid=thread-a:r4786320566051741539&simpl=msg-a:r20531779400…
            1/1"""
)

query = "Analyse the given documents" # You can play around with this and evaluate the responses

# 2 - Define template for prompts - Modify this to improve performance
template = """You are an AI Project Manager specializes in extracting important information from the given emails \
and whatsapp messages. Use the retrieved context to answer the question. Use the JSON format below to add the relevant \
data. You must analyze the conversations and understand what task is being discussed. You must also identify the people \
who are involved. You must also attach TAGs to the data. You must also identify the status of the task. You must also \
identify the date of the task. You must also identify the ID of the task. You must use the entire context to respond \
with only one task json object.

Use the following JSON format:
{{
    "ID": "The ID of the task",
    "Description": "The description of the task",
    "People: ["person 1", "person 2"],
    "Date" "date",
    "TAG": ["Unique Identifier related to the Project"],
    "Status": "Completed, Processing, On-hold, In Transit or Rejected"
}}

CONTEXT:
{context}

QUESTION: 
{question}
"""

# 3 - Create prompt template
prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)
    
# 4 - Initialize the LLM
chat_llm = ChatOpenAI(
    openai_api_key="",
    model= "gpt-3.5-turbo", # You can change the model here
    temperature=0,
    verbose=True,
    model_kwargs={"response_format": {"type": "json_object"}}, # This enforces the JSON format
)

# 5 - Initialize the Chain
chain = load_qa_chain(
    llm = chat_llm,
    chain_type = "stuff",
    prompt = prompt,
    verbose = True
)

# 6 - Running the Chain to get the response
response = chain.run(
    input_documents = [data], # An array of documents
    question = query # The actual question
)

print(response)

# 7 - Loading the response object 
response_obj = json.loads(response)

# 8 - Store in CSV
flattened = {}
for key, value in response_obj.items():
    if isinstance(value, list):
        flattened[key] = ', '.join(value)
    else:
        flattened[key] = value
        
with open("data.csv", mode='a+', newline='') as file: # You can modify the file name here
    writer = csv.DictWriter(file, fieldnames=flattened.keys())
    
    if file.tell() == 0:
        writer.writeheader()
    
    writer.writerow(flattened)