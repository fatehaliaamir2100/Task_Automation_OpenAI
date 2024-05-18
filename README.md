# Task_Automation_OpenAI

So I wanted to see if it was possible for us to use OpenAI to automate some of our most mundane tasks and I wanted to test it out to the limit. The solution presented isn’t perfect but it’s a good starting point. So I decided to throw in emails and WhatsApp messages and I asked OpenAI to detect and extract useful information about any sort of tasks that were being talked about.
So this meant that if Person A is texting Person B that you have to deliver pizza to a certain location, that task should automatically be added to our list without any human intervention whatsoever. The list should also be updated and modified accordingly as well. This is the starting point towards this kind of automation.

Powered by LangChain, this prototype solution can be reinforced towards automating any kind of conversation. Despite the amazing implications of this solution, it is still too costly for some of us. To bypass that, it is possible to run the LLM models locally and that's something I will be exploring next. For now, check out this solution and let me know what you think.

List of Packages:
/nfrom langchain.prompts import PromptTemplate
/nfrom langchain_openai import ChatOpenAI, OpenAI
/nfrom langchain.memory import ConversationBufferMemory
/nfrom langchain.chains.question_answering import load_qa_chain
/nimport csv
/nimport json
/nfrom langchain.schema import Document
