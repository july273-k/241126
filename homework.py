import streamlit as st

st.set_page_config(page_title="데이터 시각화 학습 활동지", layout="wide")

# 사이드바 메뉴
page = st.sidebar.selectbox("페이지 선택", ["활동1: 역사적 사례 탐구", "활동2: 데이터 시각화 기법 이해", "활동3: 시각화 결과 공유 및 개선"])

if page == "활동1: 역사적 사례 탐구":
    st.title("활동1: 역사적 사례를 통한 데이터 시각화 중요성 탐구")
    st.write("**이름:** (입력란)")
    st.write("**모둠:** (입력란)")
    st.write("**일자:** (입력란)")

# 나이팅게일의 로즈 다이어그램 이미지
    st.subheader("A. 나이팅게일의 로즈 다이어그램 관찰하기")

# 이미지 삽입 (이미지를 base64로 인코딩하거나, static 폴더 사용 가능)
    rose_img_path = "nightingale_rose_diagram.png"  # 예: 같은 폴더 내 이미지
    st.text_area("관찰 포인트 (예: 원형 패턴, 색상, 시간 추이 등)", "")
    st.write("2. 이 다이어그램을 통해 나이팅게일이 전달하려 한 메시지와 시각화의 이점을 생각해보세요.")
    st.text_area("전달 메시지 및 이점", "")

    st.subheader("B. 존 스노우의 콜레라 지도 분석하기")
    snow_map_path = "john_snow_cholera_map.png" 
    st.write("1. 지도 이미지 관찰: 지도 위에 어떤 정보가 표시되어 있나요?")
    st.text_area("지도 관찰 포인트 (우물 위치, 환자 발생 가구 등)", "")
    st.write("2. 시각화가 콜레라 확산 원인을 파악하는 데 어떤 도움을 주었나요?")
    st.text_area("지도 시각화의 도움", "")

    st.subheader("C. 종합 질문")
    st.write("1. 로즈 다이어그램과 콜레라 지도에서 공통적으로 발견되는 데이터 시각화의 장점을 정리해보세요.")
    st.text_area("데이터 시각화 공통 장점", "")
    st.write("2. 수치 데이터만 제시될 때와 시각화가 제공될 때의 차이를 비교해보세요.")
    st.text_area("비교 (수치만 vs 시각화)", "")


elif page == "활동2: 데이터 시각화 기법 이해":
    st.title("활동2: 다양한 데이터 시각화 기법 이해 및 적용")
    st.write("**이름:** (입력란)")
    st.write("**모둠:** (입력란)")
    st.write("**일자:** (입력란)")

    st.subheader("A. 다양한 시각화 기법 이해")
    st.write("아래 표를 참조하여 각 기법의 특징과 활용 상황을 정리해보세요.")

    st.markdown("""
    | 시각화 기법 | 특징 | 주로 활용하는 상황 | 장점 | 단점 |
    |-------------|-------|-------------------|------|------|
    | 막대 그래프  | (입력) | (입력) | (입력) | (입력) |
    | 파이 차트    | (입력) | (입력) | (입력) | (입력) |
    | 선 그래프    | (입력) | (입력) | (입력) | (입력) |
    | 히트맵(지도) | (입력) | (입력) | (입력) | (입력) |
    | 네트워크 다이어그램 | (입력) | (입력) | (입력) | (입력) |
    """)

    st.subheader("B. 데이터 시각화 실습 준비")
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
       
    else:
        st.info("CSV 파일을 업로드해주세요.")


elif page == "3차시: 시각화 결과 공유 및 개선":
    st.title("3차시: 시각화 결과 공유 및 개선")
    st.write("**이름:** (입력란)")
    st.write("**모둠:** (입력란)")
    st.write("**일자:** (입력란)")

    st.subheader("A. 시각화 결과물 공유")
    st.write("1. 다른 모둠의 시각화를 보고 인상 깊었던 점을 적어보세요.")
    st.text_area("인상 깊었던 점", "")
    st.write("2. 개선 아이디어나 질문을 적어보세요.")
    st.text_area("개선 아이디어/질문", "")

    st.subheader("B. 데이터 해석 및 활용 방안 모색")
    st.write("1. 우리 모둠 시각화를 바탕으로 문제 해결 방안이나 정책 제안을 고민해보세요.")
    st.text_area("문제 해결/정책 제안", "")
    st.write("2. 시각화 자료를 개선할 수 있는 방법을 생각해보세요.")
    st.text_area("개선 방안", "")

    st.subheader("C. 총괄 반성")
    st.write("1. 이번 활동을 통해 배운 점을 정리하세요.")
    st.text_area("배운 점", "")
    st.write("2. 다른 주제에도 데이터 시각화를 활용한다면 어떤 점이 유용할까요?")
    st.text_area("활용 방안", "")
