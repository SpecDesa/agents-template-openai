from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
        ChatPromptTemplate,
        HumanMessagePromptTemplate,
        MessagesPlaceholder
        )
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
load_dotenv()


chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(content=(
                                   "You are an AI that have access to an SQLITE database.\n"
                                   f"The database has tables of: {tables}\n"
                                   "Do not make any assumptions about what tables exist "
                                   "or what columns exist. Instead use the 'describe_tables' function"
                                   )
                          ),
            # Add here, so it comes before any new message(History before new events)
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
            # kind of similar to memory, (msg, functions) -> + ai message -> full msg to llm
            MessagesPlaceholder(variable_name="agent_scratchpad")
            ],
        input_variables=["input"]
        )

# 
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [run_query_tool, describe_tables_tool, write_report_tool]
agent = OpenAIFunctionsAgent(
        llm=chat,
        prompt=prompt,
        tools=tools
        )

agent_executor = AgentExecutor(
        agent=agent,
        verbose=True,
        tools=tools,
        memory=memory
        )


# agent_executor("How many users are in the database?")
# agent_executor("How many users have provided a shipping address?")
# agent_executor("Summarize the top 5 most popular products. Write the results to a report file.")
agent_executor(
        "How many orders are there? Write the result to an html report."
               )

# Only works if there is some "memory" to llm
agent_executor(
        "Repeat the exact same process for users."
               )

