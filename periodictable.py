import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 데이터 로드
file_path = 'elementdatavalues.csv'  # 데이터 파일 경로
try:
    element_data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    st.stop()

# 필수 열 목록
required_columns = ["Name", "Symbol", "Atomic_Number", "Graph.Period", "Graph.Group", "Electronegativity", "Atomic_Radius", "Ionization_Energy"]

# 누락된 열 확인 및 처리
missing_columns = [col for col in required_columns if col not in element_data.columns]

if missing_columns:
    for col in missing_columns:
        st.warning(f"데이터 파일에 누락된 열이 있습니다: {col}. 기본값 NaN으로 추가합니다.")
        element_data[col] = float('nan')  # NaN 값으로 누락된 열 추가

# 시각화 가능한 성질 정의
available_properties = {
    "Electronegativity": "전기음성도",
    "Atomic_Radius": "원자 반지름 (pm)",
    "Ionization_Energy": "이온화 에너지 (kJ/mol)"
}

# 데이터셋에 존재하는 열만 선택
valid_properties = {key: value for key, value in available_properties.items() if key in element_data.columns}

if not valid_properties:
    st.error("데이터셋에 시각화할 성질이 없습니다. 데이터 파일을 확인하세요.")
    st.stop()

# 사용자 선택: 시각화할 성질
selected_property = st.selectbox("시각화할 성질을 선택하세요:", options=valid_properties.keys(), format_func=lambda x: valid_properties[x])

# 데이터 전처리: 범위 계산 (NaN 값 제외)
property_min = element_data[selected_property].dropna().min()
property_max = element_data[selected_property].dropna().max()

# Matplotlib로 주기율표 시각화
st.subheader("주기율표 시각화")
fig, ax = plt.subplots(figsize=(12, 6))

# Plotting 원소별 데이터
for _, row in element_data.iterrows():
    try:
        if pd.isna(row['Graph.Period']) or pd.isna(row['Graph.Group']):
            continue
        period = int(row['Graph.Period'])
        group = int(row['Graph.Group'])

        # 데이터 점 색상 매핑
        value = row[selected_property]
        color = sns.color_palette("coolwarm", as_cmap=True)((value - property_min) / (property_max - property_min)) if not pd.isna(value) else "gray"

        ax.scatter(group, period, s=300, color=color, edgecolors="black", alpha=0.8)
        ax.text(group, period, row["Symbol"], ha="center", va="center", fontsize=10, color="white")
    except Exception as e:
        st.warning(f"데이터 오류: {row['Symbol']} - {e}")

ax.set_xlim(0.5, 18.5)
ax.set_ylim(0.5, 7.5)
ax.set_xticks(range(1, 19))
ax.set_yticks(range(1, 8))
ax.set_xlabel("Group (족)")
ax.set_ylabel("Period (주기)")
ax.set_title(f"주기율표 ({valid_properties[selected_property]})", fontsize=16)
ax.grid(True, linestyle="--", alpha=0.5)

# Streamlit에 Matplotlib 그래프 표시
st.pyplot(fig)

# Plotly로 상호작용 그래프 생성
st.subheader("원소 특성 상호작용 그래프")

# 선택한 성질을 기준으로 데이터 시각화
fig = px.scatter(
    element_data,
    x="Atomic_Number",
    y=selected_property,
    hover_name="Name",
    hover_data=["Symbol", "Electronegativity", "Atomic_Radius", "Ionization_Energy"],
    color=selected_property,
    color_continuous_scale="Viridis",
    title=f"{valid_properties[selected_property]}에 따른 원소 분포",
    labels={"Atomic_Number": "원자번호", selected_property: valid_properties[selected_property]}
)

# Streamlit에 Plotly 그래프 표시
st.plotly_chart(fig)

# 사용자 선택 원소 데이터
st.subheader("원소 데이터 탐색")
selected_symbol = st.selectbox("원소를 선택하세요:", element_data["Symbol"].sort_values())
selected_row = element_data[element_data["Symbol"] == selected_symbol].iloc[0]

# 선택된 원소 데이터 출력
value_display = selected_row[selected_property]
value_display = "데이터 없음" if pd.isna(value_display) else value_display

st.markdown(f"""
**선택한 원소 정보**
- **이름**: {selected_row['Name']}
- **기호**: {selected_row['Symbol']}
- **원자번호**: {selected_row['Atomic_Number']}
- **족(Group)**: {selected_row['Graph.Group']}
- **주기(Period)**: {selected_row['Graph.Period']}
- **{valid_properties[selected_property]}**: {value_display}
""")
