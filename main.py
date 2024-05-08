from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
        ChatPromptTemplate,
        HumanMessagePromptTemplate,
        MessagesPlaceholder
        )
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables

load_dotenv()


chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(content=f"You are an AI that have access to an SQLITE database.\n{tables}"),
            HumanMessagePromptTemplate.from_template("{input}"),
            # kind of similar to memory, (msg, functions) -> + ai message -> full msg to llm
            MessagesPlaceholder(variable_name="agent_scratchpad")
            ],
        input_variables=["input"]
        )


tools = [run_query_tool]
agent = OpenAIFunctionsAgent(
        llm=chat,
        prompt=prompt,
        tools=tools
        )

agent_executor = AgentExecutor(
        agent=agent,
        verbose=True,
        tools=tools
        )


# agent_executor("How many users are in the database?")
agent_executor("How many users have provided a shipping address?")

