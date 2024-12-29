# QR 코드 생성 도구 클래스
import qrcode
import uuid
from django.conf import settings
import os
from langchain.agents import AgentExecutor, BaseMultiActionAgent, Tool, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish
import re
import datetime



        
        
        
class QRCodeTool(BaseTool):
    name = "QRCodeTool"
    description = "A tool to generate QR codes"
    def _run(self, text: str):
        # QR 코드 생성 로직
        qr = qrcode.make(text)
        file_name = f"qr_code_{uuid.uuid4().hex}.png"
        
        # STATICFILES_DIRS 중 첫 번째 경로를 사용 (예시)
        file_path = os.path.join(settings.STATICFILES_DIRS[0], file_name)
        try:
            qr.save(file_path)
            return file_name  # 파일 이름만 반환
        except Exception as e:
            print(f"Error saving QR code: {e}")
            return None

    # def _run(self, text: str):
    #     # 텍스트를 받아 QR 코드 생성
    #     qr = qrcode.make(text)

    #     # 파일 이름 생성
    #     file_name = f"qr_code_{uuid.uuid4().hex}.png"
        
    #     # static 디렉토리 내에 파일 경로 설정
    #     file_path = os.path.join(settings.BASE_DIR, 'static', file_name)

    #     try:
    #         # QR 코드 파일 저장
    #         qr.save(file_path)
    #         return file_name  # 파일 이름 반환
    #     except Exception as e:
    #         print(f"Error saving QR code: {e}")
    #         return None

    def act(self, text: str):
        return self._run(text)

# 클래스 인스턴스 생성
qr_code_tool = QRCodeTool()






# class QRCodeTool(BaseTool):
#     name = "QRCodeTool"
#     description = "A tool to generate QR codes"

#     def _run(self, text: str):
#         # 텍스트를 받아 QR 코드 생성 및 저장
#         qr = qrcode.make(text)
#         file_path = f"qr_code_{uuid.uuid4().hex}.png"
#         try:
#             qr.save(file_path)
#             return file_path
#         except Exception as e:
#             print(f"Error saving QR code: {e}")
#             return None

#     def act(self, text: str):
#         return self._run(text)
    
# # 클래스 인스턴스 생성
# qr_code_tool = QRCodeTool()