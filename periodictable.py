import streamlit as st
import pandas as pd

# 데이터 로드
file_path = 'elementdatavalues.csv'  # 파일 경로
elements_df = pd.read_csv(file_path)

# Streamlit 제목
st.title("인터랙티브 주기율표")

# 데이터 전처리
elements_df['Graph.Period'] = elements_df['Graph.Period'].astype(int)
elements_df['Graph.Group'] = elements_df['Graph.Group'].astype(int)

# 주기율표 UI 생성
st.markdown("""
<style>
.periodic-table {
    display: grid;
    grid-template-columns: repeat(18, 50px);
    grid-gap: 5px;
    text-align: center;
    font-size: 12px;
}
.element {
    border: 1px solid #aaa;
    border-radius: 5px;
    padding: 10px;
    text-align: center;
    cursor: pointer;
}
.selected {
    background-color: #ffeb3b;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 선택된 원소를 저장하기 위한 상태
if "selected_symbol" not in st.session_state:
    st.session_state["selected_symbol"] = None

def render_periodic_table():
    # HTML 테이블 생성
    table_html = '<div class="periodic-table">'
    for _, row in elements_df.iterrows():
        symbol = row['Symbol']
        group = row['Graph.Group']
        period = row['Graph.Period']

        # 위치 계산
        grid_position = f"grid-column: {group}; grid-row: {period};"
        is_selected = st.session_state["selected_symbol"] == symbol
        css_class = "selected" if is_selected else "element"
        table_html += f'<div class="{css_class}" style="{grid_position}" onclick="document.location.href=\'#{symbol}\'">{symbol}</div>'
    
    table_html += '</div>'
    return table_html

# 주기율표 표시
st.markdown(render_periodic_table(), unsafe_allow_html=True)

# 선택된 원소 정보 표시
selected_symbol = st.selectbox("원소 선택", elements_df["Symbol"].sort_values())
selected_element = elements_df[elements_df["Symbol"] == selected_symbol].iloc[0]

st.markdown(f"""
**원소 정보**  
- 이름: {selected_element['Name']}  
- 기호: {selected_element['Symbol']}  
- 원자번호: {selected_element['Atomic_Number']}  
- 원자량: {selected_element['Atomic_Weight']}  
- 밀도: {selected_element['Density']} g/cm³  
- 족: {selected_element['Graph.Group']}  
- 주기: {selected_element['Graph.Period']}  
- 상태: {selected_element['Phase']}
""")
