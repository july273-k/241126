import streamlit as st
import pandas as pd

# 데이터 로드
file_path = 'elementdatavalues.csv'  # 데이터 파일 경로
try:
    element_data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("데이터 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    st.stop()

# 필수 컬럼 확인
required_columns = ["Name", "Symbol", "Atomic_Number", "Atomic_Weight", "Graph.Period", "Graph.Group", "Phase"]
missing_columns = [col for col in required_columns if col not in element_data.columns]

if missing_columns:
    st.error(f"데이터 파일에 누락된 컬럼이 있습니다: {', '.join(missing_columns)}")
    st.stop()

st.title("Interactive Periodic Table")

# 안전한 데이터 접근
if element_data.empty:
    st.error("데이터가 비어 있습니다. 데이터를 확인하세요.")
    st.stop()

# 선택 상자 추가
selected_symbol = st.selectbox("원소를 선택하세요:", element_data["Symbol"].sort_values())

# 선택한 원소의 데이터 가져오기
selected_row = element_data[element_data["Symbol"] == selected_symbol]
if selected_row.empty:
    st.error("선택한 원소 데이터를 찾을 수 없습니다.")
    st.stop()

selected_element = selected_row.iloc[0]  # 안전한 행 접근

# 원소 정보 출력
st.markdown(f"""
**원소 정보**
- **이름**: {selected_element['Name']}
- **기호**: {selected_element['Symbol']}
- **원자번호**: {selected_element['Atomic_Number']}
- **원자량**: {selected_element['Atomic_Weight']}
- **족**: {selected_element['Graph.Group']}
- **주기**: {selected_element['Graph.Period']}
- **상태**: {selected_element['Phase']}
""")

# 주기율표 배열 초기화
grid_template = [["" for _ in range(18)] for _ in range(7)]
lanthanides = []
actinides = []

# 배열에 데이터 삽입
for _, row in element_data.iterrows():
    try:
        period = row['Graph.Period']
        group = row['Graph.Group']

        # 란타넘족과 악티늄족 처리
        if period == 8.5:
            lanthanides.append(row['Symbol']) if group <= 17 else None
            continue
        elif period == 9.5:
            actinides.append(row['Symbol']) if group <= 17 else None
            continue

        # 일반 원소 처리
        period = int(period) - 1  # 0부터 시작하는 인덱스
        group = int(group) - 1   # 0부터 시작하는 인덱스

        # 유효성 검증
        if not (0 <= period < 7 and 0 <= group < 18):
            st.warning(f"잘못된 위치 정보: {row['Symbol']} (Period: {row['Graph.Period']}, Group: {row['Graph.Group']})")
            continue

        grid_template[period][group] = row['Symbol']
    except (ValueError, IndexError) as e:
        st.warning(f"데이터 오류: {row['Symbol']} - {e}")

# 주기율표 HTML 생성
table_html = """
<style>
.periodic-table {
    display: grid;
    grid-template-columns: repeat(18, 40px);
    grid-gap: 5px;
    text-align: center;
    font-size: 12px;
}
.element {
    border: 1px solid #aaa;
    padding: 5px;
    border-radius: 5px;
    width: 40px;
    height: 40px;
}
.selected {
    background-color: #ffeb3b;
    font-weight: bold;
}
</style>
<div class="periodic-table">
"""

for row in grid_template:
    for symbol in row:
        css_class = "selected" if symbol == selected_symbol else "element"
        table_html += f'<div class="{css_class}">{symbol}</div>' if symbol else '<div class="element"></div>'
table_html += "</div>"

# 주기율표 렌더링
st.markdown(table_html, unsafe_allow_html=True)

# 란타넘족과 악티늄족 렌더링
st.markdown("### Lanthanides (란타넘족)")
st.write(", ".join(lanthanides))

st.markdown("### Actinides (악티늄족)")
st.write(", ".join(actinides))

st.write("선택한 원소는 노란색으로 강조 표시됩니다.")
