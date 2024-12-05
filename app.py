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
            "Calcium"
        ],
        "Symbol": ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca"],
        "Atomic_Number": list(range(1, 21)),
        "Group": [1, 18, 1, 2, 13, 14, 15, 16, 17, 18, 1, 2, 13, 14, 15, 16, 17, 18, 1, 2],
        "Period": [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4],
        "Atomic_Mass": [1.008, 4.0026, 6.94, 9.0122, 10.81, 12.011, 14.007, 15.999, 18.998, 20.18, 22.99, 24.305, 26.982, 28.085, 30.974, 32.06, 35.45, 39.948, 39.098, 40.078],
        "Atomic_Radius": [53, 31, 167, 112, 87, 67, 56, 48, 42, 38, 186, 160, 143, 118, 110, 104, 99, 71, 243, 194],
        "Ionization_Energy": [1312, 2372, 520, 899, 801, 1086, 1402, 1314, 1681, 2081, 496, 737, 577, 786, 1012, 999, 1251, 1521, 418, 590],
        "Electronegativity": [2.2, None, 0.98, 1.57, 2.04, 2.55, 3.04, 3.44, 3.98, None, 0.93, 1.31, 1.61, 1.9, 2.19, 2.58, 3.16, None, 0.82, 1],
        "Density": [0.000089, 0.000178, 0.534, 1.85, 2.34, 2.27, 0.00125, 0.00143, 0.0017, 0.0009, 0.97, 1.74, 2.7, 2.33, 1.82, 2.07, 0.00321, 0.00178, 0.862, 1.54],
        "Melting_Point": [14, None, 180, 1287, 2300, 3800, 63, 54, 85, None, 98, 650, 933, 1687, 317, 388, 172, None, 336, 1115],
        "Boiling_Point": [20, None, 1342, 2471, 3930, 4300, 77, 90, 85, None, 883, 1090, 2740, 3538, 550, 717, 239, None, 1032, 1757]
    }
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)  # 결측값 처리
    return df

df = load_data()

# 선택 가능한 속성 목록
properties = ["Atomic_Mass", "Atomic_Radius", "Ionization_Energy", "Electronegativity", "Density", "Melting_Point", "Boiling_Point"]

# 레이아웃 구성
upper, lower = st.columns([1, 1])

# 상단: 인터랙
