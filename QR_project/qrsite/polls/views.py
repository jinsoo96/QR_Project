from django.shortcuts import render
# views.py

import pandas as pd
from .models import QRCodeModel
from django.http import HttpResponse
from .tools import QRCodeTool
import asyncio
from .agent_config import agent_executor
from .agents import *
import os 
from qrsite.settings import *
from urllib.parse import unquote
from django.conf import settings
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
import asyncio
from .agent_config import agent_executor
from .tools import QRCodeTool
from .models import QRCodeModel

def summarize_medical_data(data):
    """
    Summarizes the last 10 entries of medical data.

    Args:
    data (pd.DataFrame): The medical data as a DataFrame.

    Returns:
    str: A summary of the last 10 entries.
    """
    # 마지막 10개 데이터 추출
    last_10 = data.tail(10)

    # 필요한 정보 요약
    period = f"{last_10['날짜'].iloc[0]}부터 {last_10['날짜'].iloc[-1]}까지"
    treatment_types = last_10['진료종류'].unique().tolist()
    conditions = last_10['처방명'].unique().tolist()
    medications = set()
    for meds in last_10['처방약'].str.split(', '):
        medications.update(meds)
    additional_actions = set()
    for actions in last_10['처방'].str.split(', '):
        additional_actions.update(actions)

    # 요약 문장 생성
    summary = f"최근 10번의 의료 데이터 결과: 기간은 {period}입니다. 진료종류로는 {'/'.join(treatment_types)}가 있었으며, 진료된 상태는 {'/'.join(conditions)}입니다. 처방된 약물로는 {'/'.join(medications)}가 있으며, 추가적인 조치로는 {'/'.join(additional_actions)}가 포함되어 있습니다."

    return summary

async def create_qr_code(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # LangChain 에이전트 실행
        agent_result = await run_agent(user_input)

        if agent_result:
            # CSV 파일 읽기 및 데이터 요약
            csv_data = pd.read_csv('kim_jinsu_medical_records.csv')
            summary = summarize_medical_data(csv_data)

            # QR 코드 생성 (에이전트 결과와 요약 정보 결합)
            combined_text = f"{agent_result}\n\n{summary}"
            qr_tool = QRCodeTool()
            file_name = qr_tool._run(combined_text)

            if file_name:
                # 정적 파일 경로 생성
                static_file_path = os.path.join(settings.STATIC_URL, file_name)
                
                # QRCodeModel 객체 생성
                QRCodeModel.objects.create(file_path=static_file_path, user_input=user_input)

                # 정적 파일 경로를 포함한 JSON 응답 반환
                return JsonResponse({"message": "QR Code created successfully", "file_path": file_name})
            else:
                return JsonResponse({"error": "Failed to create QR Code"}, status=500)
        else:
            return JsonResponse({"error": "Failed to process input with LangChain agent"}, status=500)


async def run_agent(user_input):
    try:
        print(f"Agent input: {user_input}")
        result = await agent_executor.arun(user_input)
        # 에이전트 결과 검사 및 처리
        if isinstance(result, tuple):
            # 튜플에서 필요한 정보 추출 (예시: 첫 번째 요소 사용)
            agent_output = result[0]  # 혹은 다른 적절한 처리
        else:
            agent_output = result
        print(f"Agent output: {agent_output}")
        return agent_output
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# views.py의 home 함수 수정

# home 뷰 함수 정의 (비동기 처리 포함)
async def home(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')


        # LangChain 에이전트 비동기 실행
        agent_result = await run_agent(user_input)
        

        # QR 코드 생성 로직
        if agent_result:
            qr_tool = QRCodeTool()
            qr_code_path = qr_tool._run(agent_result)

            # QR 코드 경로의 유효성 검사
            if qr_code_path:
                # QRCodeModel 객체 생성 및 저장
                QRCodeModel.objects.create(file_path=qr_code_path, user_input=user_input)
                # 성공 시 결과 페이지로 리디렉션
                return redirect('result', qr_code_path=qr_code_path)
            else:
                # QR 코드 생성 실패
                return render(request, 'home.html', {'error': 'QR 코드 생성에 실패했습니다.'})
        else:
            # 에이전트 실행 실패
            return render(request, 'home.html', {'error': 'LangChain 에이전트 처리 실패'})

    # GET 요청 처리 (기본 홈 페이지 렌더링)
    return render(request, 'home.html')





def result(request, qr_code_path):
    return render(request, 'result.html', {'qr_code_path': qr_code_path})




async def some_view(request):
    user_input = request.GET.get('input', '')
    response = await run_agent(user_input)
    # response를 처리하여 사용자에게 반환