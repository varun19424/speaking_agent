from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.chat_models import ChatOpenAI

def get_agent_executor(tools, memory):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )
