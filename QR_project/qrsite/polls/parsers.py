import qrcode
import uuid
from langchain.agents import AgentExecutor, BaseMultiActionAgent, Tool, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union

# 출력 파서 클래스
class MyOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "Final Answer:" in llm_output:
            return AgentFinish(return_values={"output": llm_output.split("Final Answer:")[-1].strip()})
        else:
            return AgentAction(tool="qr_code_tool", tool_input=llm_output, log=llm_output)
