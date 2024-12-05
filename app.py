import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정 (코드의 가장 첫 번째 위치)
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

# 나머지 기능은 동일
