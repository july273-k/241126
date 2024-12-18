import streamlit as st
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import base64

# ------------------------------------------------------------
# Google Sheets API 설정 (예시)
# 해당 부분은 실제 서비스 계정 JSON 키 파일 경로 및 SHEET_ID를 자신의 환경에 맞게 수정해야 함
SCOPE = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
CREDS_JSON = "credentials.json" # 서비스계정 키 파일명 (실사용 시 교체)
SHEET_ID = "YOUR_GOOGLE_SHEET_ID" # 본인 구글 시트 ID로 교체
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
    # data_dict = {"학급":..., "번호":..., "이름":..., "활동":..., "답변":...}
    wks = get_worksheet(sheet_name)
    # 맨 뒤에 append
    wks.append_row(list(data_dict.values()))


# 간단한 툴팁/팝오버 CSS/HTML
tooltip_css = """
<style>
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black; 
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 250px;
  background-color: #555;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 8px;
  position: absolute;
  z-index: 1;
  bottom: 125%; /* 위치 조정 */
  left: 50%;
  margin-left: -125px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.85em;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
.zoom-img {
  transition: transform 0.2s;
  cursor: zoom-in;
}

.zoom-img:hover {
  transform: scale(1.2);
}
</style>
"""
st.markdown(tooltip_css, unsafe_allow_html=True)

def tooltip_text(term, definition):
    return f'<span class="tooltip">{term}<span class="tooltiptext">{definition}</span></span>'

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
            # 간단히 비밀번호 체크: 실제로는 DB나 시트에서 검증 필요
            if password.strip() != "":
                st.session_state.logged_in = True
                st.session_state.user_info = {
                    "학급": class_name,
                    "번호": student_num,
                    "이름": student_name,
                    "비밀번호": password
                }
                st.session_state.is_teacher = False
                st.experimental_rerun()
            else:
                st.error("비밀번호를 입력하세요.")

    else: # 교사 로그인
        teacher_id = st.text_input("교사 ID")
        teacher_pw = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            # 간단히 하드코딩
            if teacher_id == "teacher" and teacher_pw == "admin123":
                st.session_state.logged_in = True
                st.session_state.is_teacher = True
                st.experimental_rerun()
            else:
                st.error("교사 인증 실패")


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

    # 나이팅게일의 로즈 다이어그램 이미지
    st.subheader("나이팅게일의 로즈 다이어그램 관찰하기")
    # 이미지 삽입 (이미지를 base64로 인코딩하거나, static 폴더 사용 가능)
    rose_img_path = "nightingale_rose.png"  # 예: 같은 폴더 내 이미지
    snow_map_path = "john_snow_map.png"     # 예: 같은 폴더 내 이미지
    
    # 이미지 표시 (hover 시 확대)
    st.markdown(f'<img src="data:image/png;base64,{base64.b64encode(open(rose_img_path, "rb").read()).decode()}" class="zoom-img" alt="Nightingale Rose Diagram" style="max-width:400px;">', unsafe_allow_html=True)
    st.write("위 이미지를 마우스로 올리면 확대됩니다.")

    # 툴팁 예시
    st.write("다이어그램을 보면, 사망 원인을 파악하기 위해 사용된 "+tooltip_text("로즈 다이어그램","나이팅게일이 군대 병원의 사망률을 나타내기 위해 고안한 원형 그래프. 색깔과 면적으로 사망 원인을 시각적으로 전달한다.")+"을 통해 공중보건 개선의 중요성을 확인할 수 있습니다.", unsafe_allow_html=True)

    answer_1 = st.text_area("나이팅게일의 다이어그램에서 관찰한 특징과 의미를 정리하세요.")
    if st.button("활동1-1 답변 저장"):
        data = {
            "학급": st.session_state.user_info["학급"],
            "번호": st.session_state.user_info["번호"],
            "이름": st.session_state.user_info["이름"],
            "활동": "활동1-나이팅게일",
            "답변": answer_1
        }
        save_data_to_gsheet("Responses", data)
        st.success("저장 완료!")

    st.subheader("존 스노우의 콜레라 지도 분석하기")
    st.markdown(f'<img src="data:image/png;base64,{base64.b64encode(open(snow_map_path, "rb").read()).decode()}" class="zoom-img" alt="John Snow Cholera Map" style="max-width:400px;">', unsafe_allow_html=True)
    st.write("마우스를 올리면 지도 확대됩니다.")
    st.write("이 지도는 "+tooltip_text("존 스노우의 콜레라 지도","1854년 런던 소호 지역의 콜레라 사망 위치를 지도 위에 표시하여 오염된 펌프(우물)와의 연관성을 밝혀낸 지도")+"입니다.", unsafe_allow_html=True)

    answer_2 = st.text_area("콜레라 지도에서 파악한 사항을 정리하세요.")
    if st.button("활동1-2 답변 저장"):
        data = {
            "학급": st.session_state.user_info["학급"],
            "번호": st.session_state.user_info["번호"],
            "이름": st.session_state.user_info["이름"],
            "활동": "활동1-콜레라지도",
            "답변": answer_2
        }
        save_data_to_gsheet("Responses", data)
        st.success("저장 완료!")

def run_activity_2():
    st.header("활동2: 데이터 시각화 기법 이해 및 인터랙티브 차트 생성")
    st.write("아래에 CSV 형식의 데이터를 업로드하고 원하는 차트 타입을 선택해보세요.")

    uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("데이터 미리보기:", df.head())

        chart_type = st.selectbox("차트 유형 선택", ["scatter", "bar", "line"])
        x_col = st.selectbox("X축 컬럼 선택", df.columns)
        y_col = st.selectbox("Y축 컬럼 선택", df.columns)
        color_col = st.selectbox("색상 그룹 컬럼(옵션)", ["None"]+list(df.columns))
        if st.button("차트 생성"):
            if color_col == "None":
                color_col = None
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col) if chart_type == "scatter" else \
                  px.bar(df, x=x_col, y=y_col, color=color_col) if chart_type == "bar" else \
                  px.line(df, x=x_col, y=y_col, color=color_col)
            st.plotly_chart(fig, use_container_width=True)

        answer_activity2 = st.text_area("이 차트를 보고 파악할 수 있는 인사이트를 정리하세요.")
        if st.button("활동2 답변 저장"):
            data = {
                "학급": st.session_state.user_info["학급"],
                "번호": st.session_state.user_info["번호"],
                "이름": st.session_state.user_info["이름"],
                "활동": "활동2-차트인사이트",
                "답변": answer_activity2
            }
            save_data_to_gsheet("Responses", data)
            st.success("저장 완료!")
    else:
        st.info("CSV 파일을 업로드해주세요.")

def run_activity_3():
    st.header("활동3: 결과 공유 및 개선 아이디어")
    st.write("이전 활동에서 얻은 결과를 바탕으로 문제 해결 방안이나 개선 아이디어를 제안해보세요.")

    answer_activity3 = st.text_area("문제 해결 방안 또는 개선 아이디어를 작성하세요.")
    if st.button("활동3 답변 저장"):
        data = {
            "학급": st.session_state.user_info["학급"],
            "번호": st.session_state.user_info["번호"],
            "이름": st.session_state.user_info["이름"],
            "활동": "활동3-개선아이디어",
            "답변": answer_activity3
        }
        save_data_to_gsheet("Responses", data)
        st.success("저장 완료!")

def teacher_dashboard():
    st.title("교사용 대시보드")

    st.write("학생들이 제출한 내용을 확인할 수 있습니다.")

    # 데이터 불러오기
    wks = get_worksheet("Responses")
    data = wks.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    st.write("전체 응답 데이터:")
    st.dataframe(df)

    # 통계 예시: 활동별 제출수
    st.subheader("활동별 제출 개수")
    count_by_activity = df["활동"].value_counts()
    st.bar_chart(count_by_activity)

    # 학급별 제출 현황
    st.subheader("학급별 제출 현황")
    count_by_class = df["학급"].value_counts()
    st.bar_chart(count_by_class)

    # 특정 학급/학생 필터링
    class_filter = st.selectbox("학급 필터", ["전체"]+list(df["학급"].unique()))
    if class_filter != "전체":
        filtered_df = df[df["학급"] == class_filter]
    else:
        filtered_df = df

    st.write("필터 적용 결과:")
    st.dataframe(filtered_df)

    # 추가 질적 평가나 피드백 기능 구현 가능(예: st.text_input 통한 추가 메모, 또 다른 시트에 저장 등)

# 메인 로직
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.is_teacher:
        teacher_dashboard()
    else:
        student_main_page()
