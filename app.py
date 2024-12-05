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
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)  # 결측값을 0으로 대체
    return df

df = load_data()

# 데이터 탐색: 주기 선택
st.subheader("데이터 탐색")
period = st.selectbox("주기를 선택하세요", sorted(df["Period"].unique()))
filtered_data = df[df["Period"] == period]

# 데이터가 비어 있는지 확인
if filtered_data.empty:
    st.error("선택한 주기에 해당하는 데이터가 없습니다.")
else:
    st.dataframe(filtered_data)

# 인터랙티브 주기율표
st.subheader("인터랙티브 주기율표")
property = st.selectbox("속성을 선택하세요", ["Electronegativity", "Atomic_Radius"], key="property")
fig = px.scatter(
    df,
    x="Group",
    y="Period",
    size=property,
    color="State",
    text="Symbol",
    hover_data=["Element", "Atomic_Number", property],
    labels={"Group": "Group", "Period": "Period"}
)
st.plotly_chart(fig)
