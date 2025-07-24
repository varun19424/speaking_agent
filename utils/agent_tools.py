from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def get_tools(retriever=None, mode="rag"):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    tools = []

    if retriever:
        rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        tools.append(Tool(
            name="PDF_QA",
            func=rag_chain.run,
            description="Answer questions from uploaded PDF using RAG."
        ))

    if mode == "global":
        tools.append(Tool(
            name="Web_Search",
            func=DuckDuckGoSearchRun().run,
            description="Search general info using DuckDuckGo."
        ))
        tools.append(Tool(
            name="Wiki_Search",
            func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
            description="Search Wikipedia for factual information."
        ))

    return tools
