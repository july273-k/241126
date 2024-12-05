import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache
def load_data():
    data = {
        "Element": ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon"],
        "Symbol": ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"],
        "Atomic_Number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Group": [1, 18, 1, 2, 13, 14, 15, 16, 17, 18],
        "Period": [1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
        "Electronegativity": [2.2, None, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, None],
        "Atomic_Radius": [53, 31, 167, 112, 87, 67, 56, 48, 42, 38],
        "State": ["Gas", "Gas", "Solid", "Solid", "Solid", "Solid", "Gas", "Gas", "Gas", "Gas"],
    }
    return pd.DataFrame(data)

df = load_data()

# 페이지 기본 설정
st.set_page_config(page_title="통합형 주기율표", layout="wide")

# 사이드바 메뉴
menu = st.sidebar.radio(
    "메뉴 선택",
    ["데이터 탐색", "주기적 경향성 분석", "과학적 개념 탐구", "나만의 주기율표 제작"]
)

# 1. 데이터 탐색
if menu == "데이터 탐색":
    st.title("원소 데이터 탐색")
    st.write("아래는 원소 데이터를 탐색할 수 있는 테이블입니다.")
    st.dataframe(df)

    st.write("선택한 원소의 상세 정보를 확인하세요.")
    element = st.selectbox("원소를 선택하세요", df["Element"].unique())
    info = df[df["Element"] == element]
    st.write(info)

# 2. 주기적 경향성 분석
elif menu == "주기적 경향성 분석":
    st.title("주기적 경향성 분석")
    st.write("원소 속성별로 주기적 경향성을 분석할 수 있습니다.")

    property = st.selectbox("분석할 속성을 선택하세요", ["Electronegativity", "Atomic_Radius"])
    fig = px.scatter(
        df,
        x="Group",
        y="Period",
        size=property,
        color=property,
        text="Symbol",
        title=f"주기율표 - {property}",
        hover_data=["Element", "Atomic_Number", property],
        labels={"Group": "Group", "Period": "Period"},
        size_max=60,
    )
    fig.update_layout(
        xaxis=dict(title="Group", dtick=1),
        yaxis=dict(title="Period", dtick=1, autorange="reversed"),
    )
    st.plotly_chart(fig)

    st.write("속성 간 상관관계를 분석해보세요.")
    fig2 = px.scatter(
        df,
        x="Atomic_Number",
        y=property,
        size="Atomic_Radius",
        color="State",
        hover_data=["Element", property],
        title=f"Atomic Number vs {property}",
    )
    st.plotly_chart(fig2)

# 3. 과학적 개념 탐구
elif menu == "과학적 개념 탐구":
    st.title("과학적 개념 탐구")
    st.write("주기적 경향성을 과학적 개념(전자 배치, 핵전하 등)으로 탐구합니다.")

    st.markdown("""
    ### 주기적 경향성 설명
    - **원자 반지름**: 족이 증가할수록 전자 껍질 수 증가로 원자 반지름이 커짐.
    - **전기음성도**: 주기가 증가할수록 핵전하 증가로 전기음성도 상승.
    """)
    st.write("아래 그래프를 통해 이러한 개념을 시각적으로 확인하세요.")

    property = st.selectbox("속성을 선택하세요", ["Electronegativity", "Atomic_Radius"])
    fig = px.line(
        df,
        x="Atomic_Number",
        y=property,
        text="Symbol",
        markers=True,
        title=f"{property}의 주기적 경향성",
        labels={"Atomic_Number": "Atomic Number", property: property},
    )
    st.plotly_chart(fig)

# 4. 나만의 주기율표 제작
elif menu == "나만의 주기율표 제작":
    st.title("나만의 주기율표 제작")
    st.write("창의적이고 맞춤형 주기율표를 설계하세요.")

    custom_color = st.color_picker("배경 색상을 선택하세요", "#FFFFFF")
    property = st.selectbox("시각화 속성을 선택하세요", ["Electronegativity", "Atomic_Radius"])

    fig = px.scatter(
        df,
        x="Group",
        y="Period",
        size=property,
        color=property,
        text="Symbol",
        title=f"나만의 주기율표 - {property}",
        hover_data=["Element", "Atomic_Number", property],
        labels={"Group": "Group", "Period": "Period"},
        size_max=60,
    )
    fig.update_layout(plot_bgcolor=custom_color)
    st.plotly_chart(fig)

    if st.button("주기율표 저장"):
        fig.write_image("custom_periodic_table.png")
        st.success("주기율표가 저장되었습니다!")
