import streamlit as st
import pandas as pd

# 간단한 예제용 원소 데이터(일부 원소만)
data = [
    {"symbol": "H",  "name": "Hydrogen",   "atomic_number": 1,  "atomic_weight": 1.008, "group": 1, "period": 1},
    {"symbol": "He", "name": "Helium",     "atomic_number": 2,  "atomic_weight": 4.0026,"group": 18,"period": 1},
    {"symbol": "Li", "name": "Lithium",    "atomic_number": 3,  "atomic_weight": 6.94,  "group": 1, "period": 2},
    {"symbol": "Be", "name": "Beryllium",  "atomic_number": 4,  "atomic_weight": 9.0122,"group": 2, "period": 2},
    {"symbol": "B",  "name": "Boron",      "atomic_number": 5,  "atomic_weight": 10.81, "group": 13,"period": 2},
    {"symbol": "C",  "name": "Carbon",     "atomic_number": 6,  "atomic_weight": 12.011,"group": 14,"period": 2},
    {"symbol": "N",  "name": "Nitrogen",   "atomic_number": 7,  "atomic_weight": 14.007,"group": 15,"period": 2},
    {"symbol": "O",  "name": "Oxygen",     "atomic_number": 8,  "atomic_weight": 15.999,"group": 16,"period": 2},
    {"symbol": "F",  "name": "Fluorine",   "atomic_number": 9,  "atomic_weight": 18.998,"group": 17,"period": 2},
    {"symbol": "Ne", "name": "Neon",       "atomic_number": 10, "atomic_weight": 20.180,"group": 18,"period": 2}
]

df = pd.DataFrame(data)

st.title("인터랙티브 주기율표")

# 원소 선택 위젯
selected_symbol = st.selectbox("원소를 선택하세요:", df["symbol"].sort_values())

selected_element = df[df["symbol"] == selected_symbol].iloc[0]

st.markdown(f"""
**원소 정보**  
- 이름: {selected_element['name']}  
- 기호: {selected_element['symbol']}  
- 원자번호: {selected_element['atomic_number']}  
- 원자량: {selected_element['atomic_weight']}  
- 주기: {selected_element['period']}  
- 족: {selected_element['group']}
""")

# 주기율표를 HTML로 렌더링 (간단히 일부 원소만 표시하는 예)
# 실제 구현 시 모든 원소를 주기별, 족별로 배치하고 CSS를 통해 보기 좋게 꾸밀 수 있음.
# 여기서는 1주기, 2주기의 일부 원소만 예시로 표시
periodic_table = """
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
<!-- 1주기 -->
<div style="grid-column: 1;" class="element {H_class}">H</div>
<div style="grid-column: 18;" class="element {He_class}">He</div>

<!-- 2주기 -->
<div style="grid-column: 1;" class="element {Li_class}">Li</div>
<div style="grid-column: 2;" class="element {Be_class}">Be</div>
<div style="grid-column: 13;" class="element {B_class}">B</div>
<div style="grid-column: 14;" class="element {C_class}">C</div>
<div style="grid-column: 15;" class="element {N_class}">N</div>
<div style="grid-column: 16;" class="element {O_class}">O</div>
<div style="grid-column: 17;" class="element {F_class}">F</div>
<div style="grid-column: 18;" class="element {Ne_class}">Ne</div>
</div>
"""

# 선택된 원소에 대해 CSS 클래스 할당
def get_class(sym):
    return "selected" if sym == selected_symbol else ""

periodic_table_formatted = periodic_table.format(
    H_class=get_class("H"),
    He_class=get_class("He"),
    Li_class=get_class("Li"),
    Be_class=get_class("Be"),
    B_class=get_class("B"),
    C_class=get_class("C"),
    N_class=get_class("N"),
    O_class=get_class("O"),
    F_class=get_class("F"),
    Ne_class=get_class("Ne")
)

st.markdown(periodic_table_formatted, unsafe_allow_html=True)

st.write("위 표에서 선택한 원소는 노란색으로 강조 표시됩니다.")
