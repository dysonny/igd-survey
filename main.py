from flask import Flask, request, jsonify, send_from_directory  # Flask 웹 프레임워크 및 관련 모듈 가져오기
from flask_cors import CORS  # CORS 지원을 위한 라이브러리
import openai  # OpenAI API 사용을 위한 라이브러리
import os  # 환경 변수와 파일 경로 관리를 위한 모듈
import json  # JSON 데이터 처리 모듈
import time  # 시간 관련 작업을 위한 모듈
from datetime import datetime  # 날짜와 시간 처리를 위한 모듈
import re  # 정규 표현식을 다루기 위한 모듈
import pytz  # 시간대 변환을 위한 라이브러리
from dotenv import load_dotenv  # .env 파일 로드를 위한 라이브러리

# .env 파일에서 환경 변수 로드
load_dotenv()

# 대한민국(KST) 시간대 설정
KST = pytz.timezone('Asia/Seoul')
app = Flask(__name__, static_folder=".",
            static_url_path="")  # 현재 디렉토리에서 정적 파일 제공

# CORS 설정 - 모든 도메인에서 API 접근 허용
CORS(app)

# OpenAI API 키 환경 변수에서 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# API 키 확인
if not openai.api_key:
    print("⚠️  경고: OPENAI_API_KEY가 설정되지 않았습니다!")
    print("   .env 파일을 확인하세요.")

# 설문 질문 리스트
QUESTIONS = [
    "1/29: 당신은 게임에 빠져 있다고 느낍니까?(예: 전에 했던 게임에 대해 생각하거나 다음에 할 게임 시간을 기다립니까? 또는 게임이 당신의 일상생활에서 매우 중요한 활동이 되었다고 생각합니까?)",  #(IGDS9-SF 1번문항)
    "2/29: 게임을 줄이거나 그만하려고 할 때, 당신은 더 많은 짜증이나 불안 또는 심지어 슬픔을 느끼게 됩니까?",
    "3/29: 만족감이나 즐거움을 얻기 위해서 게임을 할 시간이 점점 더 많이 필요하다고 느낍니까?",
    "4/29: 게임을 조절하거나 중단하려고 노력할 때 실패하게 됩니까?",  #(IGDS9-SF 4번문항)
    "5/29: 게임 때문에 이전에 즐기던 취미나 여가활동에 흥미를 잃었습니까?",  #(IGDS9-SF 5번문항)
    "6/29: 인간관계에 문제가 된다는 것을 알면서도 게임을 계속하게 됩니까?",  #(IGDS9-SF 6번문항)
    "7/29: 가족, 치료자 또는 다른 사람에게 게임을 얼마나 오래하는지를 속인 적이 있습니까?",  #(IGDS9-SF 7번문항)
    "8/29: 부정적 감정(예: 무력감, 죄책감, 불안 등)으로부터 잠시 도망치거나 이런 감정을 달래기 위하여 게임을 합니까?",  #(IGDS9-SF 8번문항)
    "9/29: 게임 때문에 중요한 인간관계나 직업적 활동을 망치거나 학업이나 진로의 기회를 잃게 되었습니까?",  #(IGDS9-SF 9번문항)
    "10/29: 게임을 오래 하느라 잠을 못 자는 경우가 종종 있다.",
    "11/29: 기분이 나아지기 위해서 게임을 하지는 않는다.",
    "12/29: 지난 한 해 동안 게임을 하는 시간이 매우 늘었다.",
    "13/29: 게임을 하지않고 있을때는 더 짜증이 난다.",
    "14/29: 게임 때문에 다른 취미생활에 흥미를 잃었다.",
    "15/29: 게임 하는 시간을 줄이고 싶지만, 그렇게 하기가 매우 어렵다.",
    "16/29: 게임을 하지 않을때에도 다음에 언제 게임을 할것인지 생각하곤 한다.",
    "17/29: 나쁜감정들을 해소하는데 도움이 되기때문에 게임을 한다.",
    "18/29: 게임에 몰두할 시간이 점점더 많이 필요하다.",
    "19/29: 게임을 못하게 되었을 때 슬프다.",
    "20/29: 내가 게임 하는 시간에 대해 가족에게 속인적 있다.",
    "21/29: 나는 내가 게임을 그만둘 수 있으리라고 생각하지 않는다.",
    "22/29: 게임은 내 삶에서 가장 많은 시간을 소비하는 활동이 된 것 같다.",
    "23/29: 골치 아픈 일들을 잊기 위해서 게임을 한다.",
    "24/29:게임을 해야 할 것을 모두 하기에는 하루 종일도 부족하다고 종종 생각한다.",
    "25/29: 어떤 이유에서든 게임을 못하게 되지 않을까 불안해지곤 한다.",
    "26/29: 게임을 하느라 나의 인간관계가 손상되었다고 생각한다.",
    "27/29: 게임을 덜 하려고 종종 노력하지만, 그렇게 할 수 없다.",
    "28/29: 게임 때문에 나의 주된 일상 활동들(직업, 교육, 가사 등)에 부정적 영향을 받지는 않는다.",
    "29/29: 게임이 내 삶의 중요한 영역들에 부정적 영향을 미친다고 믿는다."
]
# 설문 상태 저장 변수 초기화
survey_status = {  # 현재 질문 인덱스와 사용자 응답 기록 관리
    "current_question_index": -2,  # 현재 질문 인덱스 (-2는 초기화 상태)
    "answers": [],  # 사용자의 답변 저장
    "user_query_count": 0  # 사용자가 질문한 횟수
}
# 사용자 정보 저장 변수
user_info = {}  # 사용자 이름, 생년월일, 성별 등 정보 저장
# 대화 기록 저장 변수 초기화
chat_history = {"user_info": {}, "messages": []}  # 대화 기록 초기화


def save_chat_history(history):
    # 사용자 이름과 생년월일 기반으로 파일명 생성
    name = user_info.get("name", "unknown").replace(" ",
                                                    "_")  # 사용자 이름 가져오고 공백 제거
    dob = user_info.get("dob", "unknown")  # 대화 기록 저장 폴더 경로 생성

    # 오늘 날짜를 기준으로 폴더 이름 생성
    today = datetime.now(pytz.utc).astimezone(KST).strftime(
        "%Y-%m-%d")  # 오늘 날짜 (KST)로 가져오기
    folder_path = os.path.join("userinfo", today)  # 저장 경로 설정

    file_name = f"{name}_{dob}.json"  # 파일명 생성

    # 폴더가 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 파일 저장
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:  # 파일을 열고 JSON 기록 저장
        json.dump(history, file, indent=4,
                  ensure_ascii=False)  # JSON 형식으로 기록 저장


# 초기화된 대화 기록 생성 함수
def initialize_chat_history():  # 새로운 대화 기록 생성 및 초기화
    global chat_history
    chat_history = {"user_info": user_info, "messages": []}  # 사용자 정보와 메시지 초기화
    save_chat_history(chat_history)  # 대화 기록 저장


# OpenAI Assistant 응답 메시지 생성 함수
def get_assistant_message():  # 설문조사 진행 기준 메시지를 반환
    return ("지난 1년간의 경험 중:\n"
            "- 1점: 전혀 그런 적 없다\n"
            "- 2점: 1년에 1-4번 정도 그랬다\n"
            "- 3점: 한 달에 1-3번 정도 그랬다\n"
            "- 4점: 1주에 한 번 이상 그랬다\n"
            "- 5점: 매일 또는 거의 매일 그렇다\n\n"
            "이 기준을 바탕으로 사용자의 입력을 분석하고 점수를 계산하세요.")


# 사용자 정보를 기반으로 컨텍스트 생성 함수
def get_user_context():  # 사용자 이름, 생년월일, 성별 정보를 기반으로 설명 생성

    name = user_info.get("name", "사용자")  # 사용자 이름 가져오기
    dob = user_info.get("dob", "알 수 없음")  # 사용자 생년월일 가져오기
    gender = user_info.get("gender", "알 수 없음")  # 사용자 성별 가져오기
    return (f"사용자의 이름은 {name}이고, 생년월일은 {dob}이며, 성별은 {gender}입니다. "
            "이 정보를 바탕으로 사용자에게 적합한 응답을 생성하세요.")


# Assistant 지침 메시지 생성 함수
def get_instruction_message():  # 설문 진행과 GPT 응답 지침 메시지 반환
    user_context = get_user_context()  # 사용자 정보를 포함한 컨텍스트 생성
    return f"""
{user_context}

1. 사용자가 1,2,3,4,5 중의 하나의 숫자로만 응답한 경우에는 어떠한 경우에도 항상 다음 질문으로 넘어간다.

2. 질문에 대해 응답을 한 다음에는 항상 아래와 같이 보내준다.
추가로 궁금한 점이 있다면 질문해주세요. 질문이 없다면 자신에게 맞는 번호를 선택해주세요.

3. 마지막 응답이 끝나면 설문이 "모두 완료되었습니다. 응답해 주셔서 감사합니다!"라고 말한 뒤 또 사용자가 채팅을 한다면 "모든 설문이 완료되었습니다."라고 말한다.

4. 이모티콘은 사용하지 않는다.

5. 모든 응답은 응답하지 않을 수 없다. 응답하기 싫다고 하는 경우에도 응답을 할 수 있도록 유도한다.

6. 문항이나, 사용자가 질문할 때 문장 단위로 줄바꿈을 해서 전달해준다.

7. 사용자에게 질문은 각 문항당 3번씩만 받을 거야. 3번 넘게 질문을 하면, 이 내용을 전달해줘:
"더이상 해당 문항에 대한 질문은 받지 않겠습니다. 설문 답변 해주세요."

8. 어떤 사용자가 물어보던 항상 같은 단어와 문장, 띄어쓰기를 사용해서 응답해야 함. 대화를 할 때는 항상 같은 형식, 단어, 문장과 질문으로 물어봐야 함. 새 채팅에서도 이전과 같은 형식과 문장으로 진행되어야 함.

9. 숫자가 아닌 질문을 하는 경우에는 질문에 적절한 응답을 준다. 사용자가 물어보는 질문에서 궁금한 점이 동일한 경우에는 모든 사용자에게 같은 응답을 주어야 한다.

10. 설문조사가 다 끝나면 GPT는 아래와 같이 무조건 응답한다.
"설문조사가 끝났습니다. 더이상 응답을 받지 않습니다."
"""


# GPT 응답 포맷팅 함수
def format_gpt_response(response):
    # 응답에 줄바꿈을 추가하여 가독성을 높이기
    return re.sub(r'([.!?])\s+', r'\1\n', response)


# 루트 경로 처리
@app.route('/')  # 웹 애플리케이션의 루트 경로
def index():  # index.html 파일을 반환
    return send_from_directory(".", "index.html")  # 현재 디렉토리에서 index.html 파일 제공


# 설문 초기화 API
@app.route('/reset', methods=['POST'])  # POST 요청으로 설문 상태 초기화
def reset_survey():  # 설문 상태와 대화 기록 초기화
    global survey_status, chat_history  # 전역 변수 사용
    survey_status = {"current_question_index": -2, "answers": []}  # 초기 상태로 설정
    chat_history = {"user_info": {}, "messages": []}  # 대화 기록 초기화
    return jsonify({"message": "설문 상태가 초기화되었습니다."})


# 사용자 정보 저장 API
@app.route('/user-info', methods=['POST'])  # POST 요청으로 사용자 정보 저장
def save_user_info():  # 사용자 정보 저장 및 초기화된 대화 기록 생성
    global user_info
    user_info = request.json  # 클라이언트로부터 JSON 데이터 가져오기
    if not user_info.get("name") or not user_info.get(
            "dob") or not user_info.get("gender") or not user_info.get(
                "gameAddictionScore"):
        return jsonify({"message": "모든 필드를 채워주세요."}), 400  # 필드가 부족하면 오류 응답 반환
    initialize_chat_history()  # 대화 기록 초기화
    return jsonify({"message": "User info saved successfully."})  # 성공 메시지 반환


# 설문 및 대화 처리 API
@app.route('/chat', methods=['POST'])  # POST 요청으로 대화 처리
def chat():  # 사용자 입력을 처리하고 적절한 응답 반환
    global survey_status  # 설문 상태 전역 변수 사용

    data = request.json  # 사용자 입력 데이터 가져오기
    user_input = data.get("user_input", "").strip()  # 사용자 입력 문자열 가져오기
    input_time = datetime.now(pytz.utc).astimezone(KST).strftime(
        '%Y-%m-%d %H:%M:%S')  # 입력 시간 기록

    # 설문 진행 중인 경우
    if 0 <= survey_status["current_question_index"] < len(QUESTIONS):
        if user_input.isdigit() and 1 <= int(user_input) <= 5:  # 버튼 클릭 (1~5)
            # 현재 질문(current_question_index)에 대한 답변 저장
            survey_status["answers"].append(user_input)
            
            # 다음 질문으로 이동
            survey_status["current_question_index"] += 1
            next_index = survey_status["current_question_index"]

            if next_index < len(QUESTIONS):  # 다음 질문이 있으면
                question = QUESTIONS[next_index]

                if next_index < 9:  # 1~9번 질문
                    button_texts = [
                        "1. 전혀 아니다", "2. 거의 아니다", "3. 때때로 그렇다", "4. 자주 그렇다",
                        "5. 매우 자주 그렇다"
                    ]
                else:  # 10번 이후 질문
                    button_texts = [
                        "1. 전혀 그렇지 않다", "2. 그렇지 않다", "3. 보통이다", "4. 그렇다",
                        "5. 매우 그렇다"
                    ]

                bot_reply = {
                    "question": question,
                    "button_texts": button_texts,
                    "additional_message":
                    "추가로 궁금한 점이 있다면 질문해주세요. 질문이 없다면 자신에게 맞는 번호를 선택해주세요."
                }
            else:  # 29번 질문까지 모두 완료
                bot_reply = {
                    "question": "설문이 완료되었습니다. 감사합니다!",
                    "button_texts": []
                }
        else:  # 텍스트 입력 (추가 질문) - 인덱스 유지
            # GPT에게 답변 요청, 인덱스는 변경하지 않음
            instruction_prompt = get_instruction_message()
            try:
                gpt_response = openai.ChatCompletion.create(
                    model="gpt-4o",  # GPT-4o 모델 사용
                    messages=[
                        {
                            "role": "system",
                            "content": instruction_prompt
                        },  # 시스템 지침
                        {
                            "role": "assistant",
                            "content": get_assistant_message()
                        },  # 초기 안내 메시지
                        {
                            "role": "user",
                            "content": user_input
                        },  # 사용자 입력
                    ],
                )
                gpt_reply = gpt_response["choices"][0]["message"][
                    "content"].strip()  # GPT 응답 가져오기
                bot_reply = {
                    "question": format_gpt_response(gpt_reply),  # 포맷팅된 응답
                    "button_texts": []
                }
            except Exception as e:  # GPT 호출 실패 처리
                print(f"GPT 호출 실패: {e}")
                bot_reply = {
                    "question": "죄송합니다. 입력을 처리하는 중 문제가 발생했습니다. 다시 시도해주세요.",
                    "button_texts": []
                }
    # 설문이 끝난 이후
    elif survey_status["current_question_index"] >= len(QUESTIONS):
        if user_input.isdigit():  # 숫자 입력 시
            bot_reply = {
                "question": "설문조사가 끝났습니다. 더이상 응답을 받지 않습니다.",
                "button_texts": []
            }
        else:  # 추가 질문 시
            bot_reply = {
                "question": "설문조사가 끝났습니다. 추가 질문은 받지 않습니다.",
                "button_texts": []
            }
    # 설문 초기 상태 (사용자 정보 입력 후 첫 질문 표시)
    elif survey_status["current_question_index"] == -2:
        # 첫 질문 (1/29) 표시하고 인덱스를 0으로 설정
        bot_reply = {
            "question":
            QUESTIONS[0],  # 첫 번째 질문 (1/29)
            "button_texts": [
                "1. 전혀 아니다", "2. 거의 아니다", "3. 때때로 그렇다", "4. 자주 그렇다",
                "5. 매우 자주 그렇다"
            ],
            "additional_message":
            "추가로 궁금한 점이 있다면 질문해주세요. 질문이 없다면 자신에게 맞는 번호를 선택해주세요.",
        }
        survey_status["current_question_index"] = 0  # QUESTIONS[0]에 대한 답변 대기
    else:  # 기타 상황 처리
        instruction_prompt = get_instruction_message()  # 지침 메시지 생성
        try:
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4o",  # GPT-4o 모델 사용
                messages=[
                    {
                        "role": "system",
                        "content": instruction_prompt
                    },  # 시스템 지침
                    {
                        "role": "assistant",
                        "content": get_assistant_message()
                    },  # 초기 안내 메시지
                    {
                        "role": "user",
                        "content": user_input
                    },  # 사용자 입력
                ],
            )
            gpt_reply = gpt_response["choices"][0]["message"]["content"].strip(
            )  # GPT 응답 가져오기
            bot_reply = {
                "question": format_gpt_response(gpt_reply),  # 포맷팅된 응답
                "button_texts": []
            }
        except Exception as e:  # GPT 호출 실패 처리
            print(f"GPT 호출 실패: {e}")
            bot_reply = {
                "question": "죄송합니다. 입력을 처리하는 중 문제가 발생했습니다. 다시 시도해주세요.",
                "button_texts": []
            }

    output_time = datetime.now(pytz.utc).astimezone(KST).strftime(
        '%Y-%m-%d %H:%M:%S')  # 응답 시간 기록
    chat_record = {  # 대화 기록 생성
        "user_input": user_input,
        "bot_reply": bot_reply,
        "input_time": input_time,
        "output_time": output_time,
    }
    chat_history["messages"].append(chat_record)  # 대화 기록에 추가
    save_chat_history(chat_history)  # 대화 기록 저장

    return jsonify(bot_reply)  # JSON 형태로 응답 반환


# 대화 기록 조회 API
@app.route('/history', methods=['GET'])  # GET 요청으로 대화 기록 반환
def get_history():  # 대화 기록 반환
    return jsonify(chat_history)  # JSON 형태로 대화 기록 반환


# 애플리케이션 실행
if __name__ == '__main__':  # 스크립트가 직접 실행될 때
    # 환경 변수에서 포트 번호 가져오기 (기본값: 5000)
    port = int(os.getenv("PORT", 5000))
    
    print("=" * 50)
    print("🚀 IGD 챗봇 설문조사 서버 시작")
    print("=" * 50)
    print(f"🌐 서버 주소: http://0.0.0.0:{port}")
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    print("⚠️  종료하려면 Ctrl+C를 누르세요")
    print("=" * 50)
    
    # Flask 애플리케이션 실행 (모든 IP에서 접근 가능)
    app.run(host='0.0.0.0', port=port, debug=False)
