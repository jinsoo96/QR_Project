import qrcode
import uuid
from langchain.agents import AgentExecutor, BaseMultiActionAgent, Tool, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union

# 멀티액션 에이전트 클래스
class MyMultiActionAgent(BaseMultiActionAgent):
    @property
    def input_keys(self):
        return ["input"]

    def plan(self, intermediate_steps, **kwargs):
        if len(intermediate_steps) == 0:
            return [AgentAction(tool="QRCodeTool", tool_input=kwargs["input"], log="")]
        else:
            return AgentFinish(return_values={"output": "QR 코드가 생성되었습니다."}, log="")


    async def aplan(self, intermediate_steps, **kwargs):
        if len(intermediate_steps) == 0:
            return [AgentAction(tool="QRCodeTool", tool_input=kwargs["input"], log="")]
        else:
            qr_code_file_name = intermediate_steps[-1].output  # QRCodeTool에서 반환된 파일 이름
            return AgentFinish(return_values={"output": qr_code_file_name}, log="QR 코드 생성 완료")





    # async def aplan(self, intermediate_steps, **kwargs):
    #         if len(intermediate_steps) == 0:
    #             return [AgentAction(tool="QRCodeTool", tool_input=kwargs["input"], log="")]
    #         else:
    #             # QRCodeTool에서 생성된 파일 이름을 가져와야 함
    #             qr_code_file_name = intermediate_steps[0].output
    #             return AgentFinish(return_values={"output": qr_code_file_name}, log="")






    # async def aplan(self, intermediate_steps, **kwargs):
    #     if len(intermediate_steps) == 0:
    #         return [AgentAction(tool="QRCodeTool", tool_input=kwargs["input"], log="")]
    #     else:
    #         return AgentFinish(return_values={"output": "QR 코드가 생성되었습니다."}, log="")






# 프롬프트 템플릿 클래스
class MyPromptTemplate(StringPromptTemplate):
    input_variables: List[str] = ["input"]
    partial_variables: List[str] = []

    def format(self, **kwargs) -> str:
        return f"Action: qr_code_tool\nAction Input: {kwargs['input']}\n"
