import streamlit as st
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import base64

# ------------------------------------------------------------
# Google Sheets API 설정 (예시)
SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
CREDS_JSON = "credentials.json"  # 서비스계정 키 파일명 (실사용 시 교체)
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"  # 본인 구글 시트 ID로 교체
# ------------------------------------------------------------

st.set_page_config(page_title="데이터 시각화 학습 활동", layout="wide")

# Session state 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "is_teacher" not in st.session_state:
    st.session_state.is_teacher = False

# Google Sheet 접근 함수
def get_worksheet(sheet_name):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_JSON, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    wks = sheet.worksheet(sheet_name)
    return wks

def save_data_to_gsheet(sheet_name, data_dict):
    wks = get_worksheet(sheet_name)
    wks.append_row(list(data_dict.values()))  # 데이터 저장

# 로그인 화면
def login_page():
    st.title("로그인 페이지")

    user_type = st.radio("사용자 유형을 선택하세요", ["학생", "교사"])
    if user_type == "학생":
        class_name = st.text_input("학급 (예: 3학년 2반)")
        student_num = st.text_input("번호")
        student_name = st.text_input("이름")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            if password.strip() != "":
                st.session_state.logged_in = True
                st.session_state.user_info = {
                    "학급": class_name,
                    "번호": student_num,
                    "이름": student_name,
                    "비밀번호": password
                }
                st.session_state.is_teacher = False
                st.rerun()  # st.experimental_rerun() → st.rerun()
            else:
                st.error("비밀번호를 입력하세요.")

    else:  # 교사 로그인
        teacher_id = st.text_input("교사 ID")
        teacher_pw = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            if teacher_id == "teacher" and teacher_pw == "admin123":
                st.session_state.logged_in = True
                st.session_state.is_teacher = True
                st.rerun()  # st.experimental_rerun() → st.rerun()
            else:
                st.error("교사 인증 실패")

# 학생 메인 페이지
def student_main_page():
    st.title(f"{st.session_state.user_info['학급']} {st.session_state.user_info['번호']}번 {st.session_state.user_info['이름']}님 반갑습니다!")
    activity = st.sidebar.selectbox("활동 선택", ["활동1: 역사적 사례 탐구", "활동2: 데이터 시각화 기법 이해", "활동3: 결과 공유 및 개선"])

    if activity == "활동1: 역사적 사례 탐구":
        run_activity_1()
    elif activity == "활동2: 데이터 시각화 기법 이해":
        run_activity_2()
    elif activity == "활동3: 결과 공유 및 개선":
        run_activity_3()

def run_activity_1():
    st.header("활동1: 역사적 사례를 통한 데이터 시각화 중요성 탐구")

    rose_img_path = "nightingale_rose.png"
    snow_map_path = "john_snow_map.png"
    
    st.subheader("나이팅게일의 로즈 다이어그램 관찰하기")
    st.markdown(f'<img src="data:image/png;base64,{base64.b64encode(open(rose_img_path, "rb").read()).decode()}" style="max-width:400px;">', unsafe_allow_html=True)
    answer_1 = st.text_area("나이팅게일의 다이어그램에서 관찰한 특징과 의미를 정리하세요.")
    if st.button("활동1 답변 저장"):
        data = {
            "학급": st.session_state.user_info["학급"],
            "번호": st.session_state.user_info["번호"],
            "이름": st.session_state.user_info["이름"],
            "활동": "활동1",
            "답변": answer_1
        }
        save_data_to_gsheet("Responses", data)
        st.success("저장 완료!")

def run_activity_2():
    st.header("활동2: 데이터 시각화 기법 이해")
    uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        chart_type = st.selectbox("차트 유형 선택", ["scatter", "bar", "line"])
        x_col = st.selectbox("X축", df.columns)
        y_col = st.selectbox("Y축", df.columns)
        if st.button("차트 생성"):
            if chart_type == "scatter":
                fig = px.scatter(df, x=x_col, y=y_col)
            elif chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col)
            else:
                fig = px.line(df, x=x_col, y=y_col)
            st.plotly_chart(fig)

def run_activity_3():
    st.header("활동3: 결과 공유 및 개선 아이디어")
    answer = st.text_area("개선 아이디어를 작성하세요.")
    if st.button("저장"):
        data = {
            "학급": st.session_state.user_info["학급"],
            "번호": st.session_state.user_info["번호"],
            "이름": st.session_state.user_info["이름"],
            "활동": "활동3",
            "답변": answer
        }
        save_data_to_gsheet("Responses", data)
        st.success("저장 완료!")

# 교사용 대시보드
def teacher_dashboard():
    st.title("교사용 대시보드")
    wks = get_worksheet("Responses")
    data = wks.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    st.write(df)

# 메인 로직
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.is_teacher:
        teacher_dashboard()
    else:
        student_main_page()
