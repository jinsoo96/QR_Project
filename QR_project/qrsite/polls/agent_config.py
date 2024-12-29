# agent_config.py
import qrcode
import uuid
from langchain.agents import AgentExecutor, BaseMultiActionAgent, Tool, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union
from .tools import QRCodeTool
from .agents import MyMultiActionAgent, LLMChain, AgentExecutor,MyPromptTemplate
from django.conf import settings
from qrsite.settings import OPENAI_API_KEY
from qrsite.settings import * 

from .parsers import *
llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)
# LLM 설정


# 에이전트 및 실행기 설정
prompt = MyPromptTemplate()
output_parser = MyOutputParser()
llm_chain = LLMChain(llm=llm, prompt=prompt)
qr_code_tool = QRCodeTool()

agent = MyMultiActionAgent(llm_chain=llm_chain, output_parser=output_parser, stop=["\n"], allowed_tools=["qr_code_tool"])
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=[qr_code_tool], verbose=True)
