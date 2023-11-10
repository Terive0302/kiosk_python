import pandas as pd
import speech_recognition as sr
import pyttsx3
"""
Python 3.8.0 base code

pip install pyaudio
추가로 하셔야 합니다.
"""
# Chatbot 데이터 읽기
chatbot_data = pd.read_excel("./chatbot_data.xlsx", engine="openpyxl")

# Rule을 dictionary 형태로 저장
chat_dic = {}
row = 0
for rule in chatbot_data['rule']:
    chat_dic[row] = rule.split('|')
    row += 1


def chat(request):
    for k, v in chat_dic.items():
        index = -1
        for word in v:
            try:
                if index == -1:
                    index = request.index(word)
                else:
                    if index < request.index(word, index):
                        index = request.index(word, index)
                    else:
                        index = -1
                        break
            except ValueError:
                index = -1
                break
        if index > -1:
            return chatbot_data['response'][k]
    return '무슨 말인지 모르겠어요'


def recognize_and_chat():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("말하세요...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("음성 인식 중...")
        text = recognizer.recognize_google(audio, language="ko-KR")
        print("인식된 텍스트:", text)

        # 음성 인식 결과를 chat 함수에 전달하여 처리
        response = chat(text)
        print("단골이 :", response)

        # pyttsx3를 사용하여 음성으로 출력
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"음성 인식 서비스에 오류가 있습니다: {e}")


if __name__ == "__main__":
    while True:
        user_input = input('텍스트 또는 음성으로 대화를 시작하세요. (exit로 종료): ')

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == '1':
            # 음성으로 전환
            recognize_and_chat()
        else:
            # 텍스트 입력을 chat 함수에 전달하여 처리
            response = chat(user_input)
            print("단골이 :", response)
