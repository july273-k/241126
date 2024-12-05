import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="통합형 주기율표", layout="wide")

# 데이터 로드
@st.cache
def load_data():
    data = {
        "Element": [
            "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon",
            "Sodium", "Magnesium", "Aluminum", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium",
            "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel",
            "Copper", "Zinc", "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton"
        ],
        "Symbol": [
            "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
            "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"
        ],
        "Atomic_Number": list(range(1, 37)),
        "Group": [1, 18, 1, 2, 13, 14, 15, 16, 17, 18, 1, 2, 13, 14, 15, 16, 17, 18, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                  12, 13, 14, 15, 16, 17, 18],
        "Period": [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                   4, 4],
        "Electronegativity": [
            2.20, None, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, None, 0.93, 1.31, 1.61, 1.90, 2.19, 2.58, 3.16, None,
            0.82, 1.00, 1.36, 1.54, 1.63, 1.66, 1.55, 1.83, 1.88, 1.91, 1.90, 1.65, 1.81, 2.01, 2.18, 2.55, 2.96, None
        ],
        "Atomic_Radius": [
            53, 31, 167, 112, 87, 67, 56, 48, 42, 38, 186, 160, 143, 118, 110, 104, 99, 71, 243, 194, 184, 176, 171, 166,
            161, 156, 152, 149, 145, 142, 136, 125, 114, 103, 94, 88
        ],
        "State": [
            "Gas", "Gas", "Solid", "Solid", "Solid", "Solid", "Gas", "Gas", "Gas", "Gas", "Solid", "Solid", "Solid",
            "Solid", "Solid", "Solid", "Gas", "Gas", "Solid", "Solid", "Solid", "Solid", "Solid", "Solid", "Solid",
            "Solid", "Solid", "Solid", "Solid", "Solid", "Solid", "Solid", "Solid", "Liquid", "Gas"
        ],
    }
    return pd.DataFrame(data)

df = load_data()

# 페이지 제목
st.title("통합형 주기율표 - 데이터 탐색과 시각화")

# 네 구역 레이아웃
upper_left, upper_right = st.columns([2, 2])
lower_left, lower_right = st.columns([2, 2])

# 좌측 상단: 인터랙티브 주기율표
with upper_left:
    st.subheader("인터랙티브 주기율표")
    property = st.selectbox("속성을 선택하세요", ["Electronegativity", "Atomic_Radius"])
    fig1 = px.scatter(
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
    fig1.update_layout(
        xaxis=dict(title="Group", dtick=1),
        yaxis=dict(title="Period", dtick=1, autorange="reversed"),
    )
    st.plotly_chart(fig1, use_container_width=True)

# 우측 상단: 원소 데이터
with upper_right:
    st.subheader("원소 데이터 탐색")
    period = st.selectbox("주기를 선택하세요", sorted(df["Period"].unique()))
    filtered_data = df[df["Period"] == period]
    st.write(f"**{period}주기 원소 데이터**")
    st.dataframe(filtered_data)

# 좌측 하단: 속성 1, 2 그래프
with lower_left:
    st.subheader("속성 1, 2의 주기적 경향성")
    prop1 = st.selectbox("속성 1", ["Electronegativity", "Atomic_Radius"], key="prop1")
    prop2 = st.selectbox("속성 2", ["Electronegativity", "Atomic_Radius"], key="prop2")
    fig2 = px.line(
        df,
        x="Atomic_Number",
        y=prop1,
        title=f"{prop1}의 주기적 경향성",
        markers=True,
        labels={"Atomic_Number": "Atomic Number", prop1: prop1},
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(
        df,
        x="Atomic_Number",
        y=prop2,
        title=f"{prop2}의 주기적 경향성",
        markers=True,
        labels={"Atomic_Number": "Atomic Number", prop2: prop2},
    )
    st.plotly_chart(fig3, use_container_width=True)

# 우측 하단: 속성 3, 4 그래프
with lower_right:
    st.subheader("속성 3, 4의 주기적 경향성")
    prop3 = st.selectbox("속성 3", ["Electronegativity", "Atomic_Radius"], key="prop3")
    prop4 = st.selectbox("속성 4", ["Electronegativity", "Atomic_Radius"], key="prop4")
    fig4 = px.line(
        df,
        x="Atomic_Number",
        y=prop3,
        title=f"{prop3}의 주기적 경향성",
        markers=True,
        labels={"Atomic_Number": "Atomic Number", prop3: prop3},
    )
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.line(
        df,
        x="Atomic_Number",
        y=prop4,
        title=f"{prop4}의 주기적 경향성",
        markers=True,
        labels={"Atomic_Number": "Atomic Number", prop4: prop4},
    )
    st.plotly_chart(fig5, use_container_width=True)
