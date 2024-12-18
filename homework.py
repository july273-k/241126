import streamlit as st

# 페이지 제목
st.title("데이터 시각화 기반 학습 활동")
st.sidebar.title("활동 선택")
activity = st.sidebar.radio("활동을 선택하세요", ["활동 1: 역사적 사례 탐구", "활동 2: 데이터 시각화 기법 이해하기", "활동 3: 시각화 결과 공유 및 개선"])

# 활동 1: 역사적 사례 탐구
if activity == "활동 1: 역사적 사례 탐구":
    st.header("활동 1: 역사적 사례 탐구")
    st.subheader("A. 나이팅게일의 로즈 다이어그램 관찰하기")
    name = st.text_input("이름")
    group = st.text_input("모둠")
    date = st.date_input("일자")
    
    st.write("### 1. 로즈 다이어그램 살펴보기")
    st.text_area("다이어그램에서 눈에 띄는 특징을 적어보세요 (예: 원형 패턴, 각 구역별 크기 차이, 색상의 의미 등)", key="rose_diagram_features")
    st.text_area("관찰 포인트를 작성하세요 (색상/모양/크기, 시간적 변화나 추세 등)", key="rose_diagram_observation")
    
    st.write("### 2. 로즈 다이어그램의 의미 해석")
    st.text_area("로즈 다이어그램의 메시지를 분석하세요", key="rose_diagram_message")
    st.text_area("시각화의 이점을 정리하세요", key="rose_diagram_advantages")
    
    st.subheader("B. 존 스노우의 콜레라 지도 분석하기")
    st.write("### 1. 콜레라 지도 살펴보기")
    st.text_area("지도에서 눈에 띄는 점을 적어보세요 (예: 특정 지역 내 우물 위치, 발병 가구 표시 등)", key="cholera_map_features")
    st.text_area("연관성 있는 요소들을 작성하세요", key="cholera_map_relations")
    
    st.write("### 2. 지도를 통한 원인 파악")
    st.text_area("콜레라 확산의 원인을 지도에서 어떻게 추론했는지 작성하세요", key="cholera_cause_analysis")
    st.text_area("지도 시각화의 중요성을 작성하세요", key="cholera_visualization_importance")
    
    st.subheader("C. 종합 질문")
    st.text_area("로즈 다이어그램과 콜레라 지도에서 공통적으로 발견되는 시각화의 장점을 정리하세요", key="common_visualization_advantages")
    st.text_area("수치 데이터와 시각화 데이터의 차이를 비교하세요", key="data_comparison")

# 활동 2: 데이터 시각화 기법 이해하기
elif activity == "활동 2: 데이터 시각화 기법 이해하기":
    st.header("활동 2: 데이터 시각화 기법 이해하기")
    st.text_area("막대 그래프의 특징, 장단점, 활용 사례를 적어보세요", key="bar_chart")
    st.text_area("파이 차트의 특징, 장단점, 활용 사례를 적어보세요", key="pie_chart")
    st.text_area("선 그래프의 특징, 장단점, 활용 사례를 적어보세요", key="line_chart")
    st.text_area("히트맵의 특징, 장단점, 활용 사례를 적어보세요", key="heatmap")
    st.text_area("네트워크 다이어그램의 특징, 장단점, 활용 사례를 적어보세요", key="network_diagram")
    
    st.subheader("B. 데이터 시각화 실습 준비")
    st.text_area("모둠별 제공된 데이터에 대해 적어보세요 (데이터 종류, 범위 등)", key="data_analysis")
    st.text_area("선택한 시각화 기법과 그 이유를 적어보세요", key="chosen_visualization")
    st.text_area("시각화 설계안을 스케치해보세요 (간단한 설명)", key="visualization_design")

# 활동 3: 시각화 결과 공유 및 개선
elif activity == "활동 3: 시각화 결과 공유 및 개선":
    st.header("활동 3: 시각화 결과 공유 및 개선")
    st.subheader("A. 시각화 결과물 공유")
    st.text_area("다른 모둠의 시각화에서 인상 깊었던 점을 적어보세요", key="other_team_highlights")
    st.text_area("개선 아이디어를 적어보세요", key="improvement_ideas")
    
    st.subheader("B. 데이터 해석 및 활용 방안 모색")
    st.text_area("문제 해결 아이디어나 정책 제안을 적어보세요", key="problem_solving_ideas")
    st.text_area("시각화 자료를 개선하기 위한 방안을 적어보세요", key="visualization_improvement")
    
    st.subheader("C. 총괄 반성")
    st.text_area("이번 활동을 통해 배운 점을 자유롭게 적어보세요", key="lesson_learned")
    st.text_area("다른 주제에서도 시각화를 활용할 방법을 적어보세요", key="future_utilization")
    
st.sidebar.write("모든 활동 결과는 다운로드 가능합니다.")
if st.sidebar.button("결과 다운로드"):
    st.write("📂 현재 활동 내용을 다운로드하세요.")
