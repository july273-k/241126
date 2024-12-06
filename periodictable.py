import streamlit as st
import pandas as pd

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

# 주기율표 배열 초기화
grid_template = [[None for _ in range(18)] for _ in range(7)]

# 데이터 삽입
for _, row in element_data.iterrows():
    try:
        if pd.isna(row['Graph.Period']) or pd.isna(row['Graph.Group']):
            continue
        period = int(row['Graph.Period']) - 1
        group = int(row['Graph.Group']) - 1

        # 유효한 범위 내에서 데이터 삽입
        if 0 <= period < len(grid_template) and 0 <= group < len(grid_template[0]):
            grid_template[period][group] = row
    except (ValueError, IndexError):
        st.warning(f"잘못된 데이터로 인해 {row['Symbol']}을(를) 추가할 수 없습니다.")

# 색상 매핑 함수
def get_color(value, min_value, max_value):
    if pd.isna(value):
        return "#cccccc"  # 값이 없는 경우 회색
    ratio = (value - min_value) / (max_value - min_value)
    blue = int(255 * (1 - ratio))
    red = int(255 * ratio)
    return f"rgb({red}, 0, {blue})"

# HTML 생성
table_html = """
<style>
.periodic-table {
    display: grid;
    grid-template-columns: repeat(18, minmax(40px, 1fr));
    grid-gap: 5px;
    text-align: center;
    font-size: 12px;
}
.element {
    border: 1px solid #aaa;
    border-radius: 5px;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
}
</style>
<div class="periodic-table">
"""

# 주기율표 HTML 렌더링
for row in grid_template:
    for cell in row:
        if cell is None:
            table_html += '<div class="element" style="background-color: #f1f1f1;"></div>'
        else:
            value = cell[selected_property]
            color = get_color(value, property_min, property_max)
            table_html += f'<div class="element" style="background-color: {color};">{cell["Symbol"]}</div>'
table_html += "</div>"

# 주기율표 출력
st.markdown(table_html, unsafe_allow_html=True)

# 선택
