import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본설정
st.set_page_config(
    page_title="주기율표 데이터 시각화 학습",
    page_icon="🔬",
    layout="wide"
)

# 세션 스테이트 초기화
if 'logged_in_student' not in st.session_state:
    st.session_state.logged_in_student = False
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'teacher_mode' not in st.session_state:
    st.session_state.teacher_mode = False

# 사이드바 탭(단계) 설정
steps = [
    "로그인창",
    "학습 목표",
    "문제 인식 단계",
    "자료 탐색 단계",
    "시각화 단계",
    "해석 단계",
    "정리·확장 단계",
    "교사용 대시보드"
]

selected_step = st.sidebar.radio("단계 선택", steps)

# 깔끔한 스타일 적용(약간의 CSS)
st.markdown("""
    <style>
    .reportview-container {
        background-color: #FBFBFB;
    }
    .sidebar .sidebar-content {
        background-color: #ECECEC;
    }
    h1, h2, h3, h4 {
        font-family: 'Helvetica', 'Arial', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 각 단계별 화면 구성 함수
def page_login():
    st.title("학생 로그인")
    st.write("학년, 반, 이름을 입력하여 등록하세요.")
    grade = st.selectbox("학년 선택", ["1학년", "2학년", "3학년"])
    classroom = st.selectbox("반 선택", [f"{i}반" for i in range(1, 11)])
    name = st.text_input("이름 입력")
    if st.button("등록하기"):
        if name.strip() != "":
            st.session_state.logged_in_student = True
            st.session_state.student_name = name.strip()
            st.success(f"{grade} {classroom} {name} 학생 환영합니다!")
        else:
            st.warning("이름을 입력해주세요.")

    st.write("---")
    st.title("교사 로그인")
    pwd = st.text_input("관리자 비밀번호 입력", type="password")
    if st.button("교사 대시보드로 이동"):
        # 여기에 실제 비밀번호 검증 로직 추가 가능
        if pwd == "teacherpass":  # 예: 'teacherpass'를 정해진 비밀번호로 가정
            st.session_state.teacher_mode = True
            st.success("교사 모드로 전환되었습니다.")
        else:
            st.warning("비밀번호가 올바르지 않습니다.")

def page_learning_goals():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return
    st.title("학습 목표")
    st.write("""
    1. 역사적 사례를 통해 데이터 시각화의 중요성을 이해한다.  
    2. 주기율표에서 특정 물리·화학적 성질(예: 원자 반지름, 이온화 에너지)을 시각화하여 주기적 경향성을 파악한다.  
    3. 원소의 전자배치나 유효 핵전하(핵 전하, 가리움효과)와 주기적 경향성 간의 상관 관계를 스스로 해석한다.
    """)

def page_problem_recognition():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return

    st.title("문제 인식 단계: 데이터 시각화의 중요성 이해하기")
    st.subheader("역사적 사례 살펴보기")
    st.write("**사례1: John Snow의 콜레라 확산 지도**")
    st.video("https://youtu.be/qf30Occ3_KI?si=U7m4yISdqC_dczrp")
    st.write("데이터(환자 발생지점)를 지도 형태로 표현 -> 콜레라 발생 원인 파악에 도움")

    st.write("**사례2: 멘델레예프의 주기율표**")
    st.video("https://youtu.be/fPnwBITSmgU?si=hiqFPCVOLjU4NWwn")
    st.write("원소 특성을 표로 조직화 -> 미발견 원소까지 예측")

    st.write("이러한 역사적 사례에서 데이터 시각화가 새로운 패턴과 법칙 발견에 기여함을 알 수 있습니다.")

def page_data_exploration():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return

    st.title("자료 탐색 단계: 원소 특성 데이터 수집 및 전처리")
    st.write("아래는 2주기 원소를 예시로 한 데이터 프레임입니다. (실제 데이터는 수업 또는 인터넷 자료 활용)")
    
    # 예시용 더미 데이터프레임
    data = {
        "원소": ["Li","Be","B","C","N","O","F","Ne"],
        "원자번호": [3,4,5,6,7,8,9,10],
        "원자량": [6.94,9.01,10.81,12.01,14.01,16.00,19.00,20.18],
        "원자 반지름(pm)": [152,112,85,77,75,73,71,38],
        "1차 이온화 에너지(kJ/mol)": [520,900,800,1086,1402,1314,1681,2081],
        "전기음성도": [0.98,1.57,2.04,2.55,3.04,3.44,3.98,"-"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.write("질문: 이러한 데이터들을 그래프로 표현한다면 어떤 패턴을 쉽게 찾을 수 있을까요?")

def page_visualization():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return

    st.title("시각화 단계: 그래프나 색상 지도로 표현하기")

    # 예시: 원자 반지름 막대 그래프
    data = {
        "원소": ["Li","Be","B","C","N","O","F","Ne"],
        "원자번호": [3,4,5,6,7,8,9,10],
        "원자 반지름(pm)": [152,112,85,77,75,73,71,38],
        "이온화 에너지(kJ/mol)": [520,900,800,1086,1402,1314,1681,2081],
        "전기음성도": [0.98,1.57,2.04,2.55,3.04,3.44,3.98,4.0]
    }
    df = pd.DataFrame(data)

    st.subheader("활동 A: 원자 반지름 막대 그래프")
    fig1 = px.bar(df, x="원자번호", y="원자 반지름(pm)", hover_data=["원소"])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("활동 B: 이온화 에너지 선 그래프")
    fig2 = px.line(df, x="원자번호", y="이온화 에너지(kJ/mol)", markers=True, hover_data=["원소"])
    st.plotly_chart(fig2, use_container_width=True)

    st.write("질문: 막대 그래프(원자 반지름)나 선 그래프(이온화 에너지)를 볼 때, 왼쪽에서 오른쪽으로 갈수록 어떤 경향성이 보이나요?")

def page_interpretation():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return
    
    st.title("해석 단계: 주기적 경향성 파악 및 원인 분석하기")

    st.write("아래 빈칸에 각 성질의 경향성을 서술해보세요.")
    st.write("원자 반지름: ________")
    st.write("이온화 에너지: ________")
    st.write("전기음성도: ________")

    st.info("""
    **정답 예시(수업 후 공개):**  
    - 원자 반지름: 같은 주기에서 왼→오른쪽으로 갈수록 감소  
    - 이온화 에너지: 같은 주기에서 왼→오른쪽으로 갈수록 증가  
    - 전기음성도: 같은 주기에서 오른쪽으로 갈수록 증가, 족에서 위로 갈수록 증가
    """)

    st.subheader("전자배치와 유효 핵전하 해석")
    st.write("주기 내 오른쪽으로 갈수록 양성자 수 증가 → 유효 핵전하 증가 → 전자들이 핵에 더 강하게 끌림 → 원자 반지름 감소, 이온화 에너지 증가, 전기음성도 증가")

def page_summary():
    if not st.session_state.logged_in_student and not st.session_state.teacher_mode:
        st.warning("로그인 후 이용 가능합니다.")
        return
    
    st.title("정리·확장 단계")

    st.write("""
    - 데이터 시각화를 통해 패턴(주기적 경향성)을 발견하고, 이를 전자배치와 유효 핵전하 개념으로 해석하였습니다.
    - 단순 암기에서 벗어나 왜 이러한 경향성을 보이는지 논리적 이해가 가능해집니다.
    """)

    st.subheader("심화 질문")
    st.write("1. 족 방향으로 변화하는 경향성(아래로 갈수록 원자 반지름 증가, 이온화 에너지 감소)은 어떻게 설명할 수 있을까요?")
    st.write("2. 다른 물리·화학적 성질(예: 전자친화도, 융점, 비점)도 비슷한 방식으로 시각화하고 패턴을 파악할 수 있을까요?")

def page_teacher_dashboard():
    if not st.session_state.teacher_mode:
        st.warning("교사만 접근 가능합니다.")
        return

    st.title("교사 대시보드")
    st.write("학생 응답 현황, 제출 그래프, 로그인 기록 등을 확인할 수 있습니다.")

    # 실제로는 수집된 학생 응답 데이터프레임 표시, 통계 차트 등 구현 가능
    # 예:
    # st.dataframe(student_responses_df)
    st.write("예시: 학생 응답 데이터 (미구현)")

# 선택된 단계에 따라 페이지 렌더링
if selected_step == "로그인창":
    page_login()
elif selected_step == "학습 목표":
    page_learning_goals()
elif selected_step == "문제 인식 단계":
    page_problem_recognition()
elif selected_step == "자료 탐색 단계":
    page_data_exploration()
elif selected_step == "시각화 단계":
    page_visualization()
elif selected_step == "해석 단계":
    page_interpretation()
elif selected_step == "정리·확장 단계":
    page_summary()
elif selected_step == "교사용 대시보드":
    page_teacher_dashboard()
