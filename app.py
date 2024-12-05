import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="통합형 주기율표", layout="wide")

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

# 페이지 제목
st.title("통합형 주기율표 - 데이터 탐색과 시각화")

# 레이아웃 구성
col1, col2 = st.columns([1, 2])

# 왼쪽: 데이터 탐색
with col1:
    st.subheader("데이터 탐색")
    st.dataframe(df)

    st.subheader("원소 상세 정보")
    element = st.selectbox("원소를 선택하세요", df["Element"].unique())
    info = df[df["Element"] == element]
    st.write(info)

# 오른쪽: 시각화
with col2:
    st.subheader("주기적 경향성 분석")

    # 속성 선택
    property = st.selectbox("분석할 속성을 선택하세요", ["Electronegativity", "Atomic_Radius"])

    # 주기적 경향성 그래프
    fig1 = px.scatter(
        df,
        x="Atomic_Number",
        y=property,
        text="Symbol",
        title=f"{property}의 주기적 경향성",
        labels={"Atomic_Number": "Atomic Number", property: property},
    )
    fig1.update_traces(marker=dict(size=12))
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("인터랙티브 주기율표")
    # 인터랙티브 주기율표
    fig2 = px.scatter(
        df,
        x="Group",
        y="Period",
        size=property,
        color="State",
        text="Symbol",
        title=f"주기율표 - {property}",
        hover_data=["Element", "Atomic_Number", property],
        labels={"Group": "Group", "Period": "Period"},
        size_max=60,
    )
    fig2.update_layout(
        xaxis=dict(title="Group", dtick=1),
        yaxis=dict(title="Period", dtick=1, autorange="reversed"),
    )
    st.plotly_chart(fig2, use_container_width=True)
