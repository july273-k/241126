import streamlit as st
import plotly.express as px
from PIL import Image

# 페이지 제목
st.title("데이터 시각화 기반 학습 활동")
st.sidebar.title("활동 선택")
activity = st.sidebar.radio("활동을 선택하세요", ["활동 1: 역사적 사례 탐구", "활동 2: 데이터 시각화 기법 이해하기", "활동 3: 시각화 결과 공유 및 개선"])

# 활동 1: 역사적 사례 탐구
if activity == "활동 1: 역사적 사례 탐구":
    st.header("활동 1: 역사적 사례 탐구")
    
    name = st.text_input("이름")
    group = st.text_input("모둠")
    date = st.date_input("일자")
    
    st.subheader("A. 나이팅게일의 로즈 다이어그램 관찰하기")
    st.write("### 1. 로즈 다이어그램 살펴보기")
    st.write("아래 이미지를 클릭하거나 마우스를 올려 확대해보세요.")
    rose_diagram = Image.open("nightingale_rose_diagram.png")  # 나이팅게일의 로즈 다이어그램 이미지 파일
    st.image(rose_diagram, caption="나이팅게일의 로즈 다이어그램", use_column_width=True)
    st.write("로즈 다이어그램은 **병사들의 사망 원인**을 시각적으로 보여줍니다.")
    
    st.text_area("눈에 띄는 특징을 적어보세요", key="rose_diagram_features")
    
    st.subheader("B. 존 스노우의 콜레라 지도 분석하기")
    st.write("### 1. 콜레라 지도 살펴보기")
    st.write("아래 이미지를 클릭하거나 마우스를 올려 확대해보세요.")
    cholera_map = Image.open("john_snow_cholera_map.jpg")  # 존 스노우 콜레라 지도 이미지 파일
    st.image(cholera_map, caption="존 스노우의 콜레라 지도", use_column_width=True)
    st.write("콜레라 지도는 **콜레라 발병의 원인을 추적**하기 위한 도구로 사용되었습니다.")
    
    st.text_area("지도에서 관찰한 점을 적어보세요", key="cholera_map_features")
    
    st.subheader("C. 종합 질문")
    st.text_area("데이터 시각화의 공통적 장점을 정리하세요", key="common_visualization_advantages")

# 활동 2: 데이터 시각화 기법 이해하기
elif activity == "활동 2: 데이터 시각화 기법 이해하기":
    st.header("활동 2: 데이터 시각화 기법 이해하기")
    
    st.subheader("A. 다양한 시각화 기법 이해")
    st.text_area("막대 그래프의 특징, 장단점, 활용 사례를 적어보세요", key="bar_chart")
    st.text_area("파이 차트의 특징, 장단점, 활용 사례를 적어보세요", key="pie_chart")
    st.text_area("선 그래프의 특징, 장단점, 활용 사례를 적어보세요", key="line_chart")
    st.text_area("히트맵의 특징, 장단점, 활용 사례를 적어보세요", key="heatmap")
    st.text_area("네트워크 다이어그램의 특징, 장단점, 활용 사례를 적어보세요", key="network_diagram")
    
    st.subheader("B. 데이터 시각화 실습 준비")
    st.text_area("모둠별 데이터 종류를 적어보세요", key="data_analysis")
    
    st.write("### 인터랙티브 차트 생성")
    st.write("아래 데이터를 입력하고 차트를 생성해보세요.")
    
    # 사용자 입력을 받아 데이터 생성
    num_points = st.number_input("데이터 포인트 수 입력", min_value=10, max_value=100, value=20)
    x_values = list(range(1, num_points + 1))
    y_values = [st.slider(f"y 값 입력 ({i+1}번 데이터)", 0, 100, 50) for i in range(num_points)]
    
    # Plotly 차트 생성
    st.write("#### 생성된 인터랙티브 차트")
    chart = px.line(x=x_values, y=y_values, labels={"x": "데이터 포인트", "y": "값"})
    st.plotly_chart(chart, use_container_width=True)

# 활동 3: 시각화 결과 공유 및 개선
elif activity == "활동 3: 시각화 결과 공유 및 개선":
    st.header("활동 3: 시각화 결과 공유 및 개선")
    
    st.subheader("A. 시각화 결과물 공유")
    st.text_area("다른 모둠의 시각화에서 인상 깊었던 점을 적어보세요", key="other_team_highlights")
    
    st.subheader("B. 데이터 해석 및 활용 방안 모색")
    st.text_area("문제 해결 아이디어를 적어보세요", key="problem_solving_ideas")
    
    st.subheader("C. 총괄 반성")
    st.text_area("배운 점을 자유롭게 적어보세요", key="lesson_learned")

st.sidebar.write("결과를 다운로드하려면 아래 버튼을 클릭하세요.")
if st.sidebar.button("결과 다운로드"):
    st.write("📂 현재 활동 내용을 다운로드하세요.")
