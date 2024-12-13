import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# 헨더슨-하셀바흐 식: pH = pKa + log([A-]/[HA])
pKa = 4.76
kw = 1e-14  # 물의 이온 곱 (25°C에서)

st.title("완충용액 공통 이온 효과 시뮬레이션")

st.write("""
이 웹 앱은 아세트산(HA) - 아세트산나트륨(A⁻) 완충용액에 산(HCl)이나 염기(NaOH), 
혹은 공통 이온(A⁻, NaA 형태)을 추가하여 공통 이온 효과를 관찰할 수 있는 시뮬레이터입니다.

- **초기 조건**: [HA]와 [A⁻] 농도를 설정  
- **조작**: 산(HCl), 염기(NaOH), 염(NaA)를 일정 농도로 추가 후 변화된 pH와 이온 농도를 확인  
- **시각화**:  
   1) 막대 그래프: HA와 A⁻의 최종 농도  
   2) 이온 모형: HA, A⁻, H⁺, OH⁻ 이온의 상대적 개수를 점으로 표현
""")

# 사이드바 설정 영역
st.sidebar.header("초기 조건 및 추가물질 설정")

col_init = st.sidebar.expander("초기 농도 설정", expanded=True)
with col_init:
    initial_HA_slider = st.slider("초기 HA 농도 (mM)", min_value=1.0, max_value=100.0, value=50.0)
    initial_HA_input = st.number_input("직접 입력 (초기 HA, mM)", value=initial_HA_slider, min_value=1.0, max_value=100.0)
    initial_HA = initial_HA_input

    initial_A_slider = st.slider("초기 A⁻ 농도 (mM)", min_value=1.0, max_value=100.0, value=50.0)
    initial_A_input = st.number_input("직접 입력 (초기 A⁻, mM)", value=initial_A_slider, min_value=1.0, max_value=100.0)
    initial_A = initial_A_input

col_add = st.sidebar.expander("물질 추가", expanded=True)
with col_add:
    add_species = st.selectbox("추가할 물질 선택", ["None", "강산(HCl)", "강염기(NaOH)", "아세트산나트륨(NaA)"])
    added_amount_slider = st.slider("추가량 (mM)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    added_amount_input = st.number_input("직접 입력 (추가량, mM)", value=added_amount_slider, min_value=0.0, max_value=100.0, step=1.0)
    added_amount = added_amount_input

# 초기 상태
HA = initial_HA
A = initial_A

# 강산(HCl) 추가
if add_species == "강산(HCl)" and added_amount > 0:
    delta = min(A, added_amount)
    A = A - delta
    HA = HA + delta
    leftover_H = added_amount - delta
    if leftover_H > 0:
        HA += leftover_H

# 강염기(NaOH) 추가
if add_species == "강염기(NaOH)" and added_amount > 0:
    delta = min(HA, added_amount)
    HA = HA - delta
    A = A + delta
    leftover_OH = added_amount - delta

# 아세트산나트륨(NaA) 추가
if add_species == "아세트산나트륨(NaA)" and added_amount > 0:
    A = A + added_amount

# pH 계산
if add_species == "강염기(NaOH)" and added_amount > 0:
    delta = min(initial_HA, added_amount)
    leftover_OH = added_amount - delta
    if leftover_OH > 0:
        OH_conc = leftover_OH * 1e-3
        pOH = -np.log10(OH_conc)
        pH = 14 - pOH
    else:
        if A > 0 and HA > 0:
            pH = pKa + np.log10(A/HA)
        else:
            if A <= 0:
                pH = 0
            elif HA <= 0:
                pH = 14
else:
    if add_species == "강산(HCl)" and added_amount > 0:
        leftover_H = added_amount - min(initial_A, added_amount)
        if leftover_H > 0:
            H_conc = leftover_H * 1e-3
            pH = -np.log10(H_conc)
        else:
            if A > 0 and HA > 0:
                pH = pKa + np.log10(A/HA)
            else:
                if A <= 0:
                    pH = 0
                elif HA <= 0:
                    pH = 14
    else:
        if A > 0 and HA > 0:
            pH = pKa + np.log10(A/HA)
        else:
            if A <= 0:
                pH = 0
            elif HA <= 0:
                pH = 14

# H⁺와 OH⁻ 농도 계산
H_conc = 10**(-pH) * 1e3  # mM 단위
OH_conc = (kw / (10**(-pH))) * 1e3  # mM 단위

# 결과 표시
st.subheader("결과")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**최종 pH**: {pH:.2f}")
    st.write(f"**최종 HA 농도**: {HA:.2f} mM")
    st.write(f"**최종 A⁻ 농도**: {A:.2f} mM")
    st.write(f"**최종 H⁺ 농도**: {H_conc:.2e} mM")
    st.write(f"**최종 OH⁻ 농도**: {OH_conc:.2e} mM")

# 농도 막대 그래프
with col2:
    fig, ax = plt.subplots(figsize=(4,3))
    ions = ["HA", "A⁻", "H⁺", "OH⁻"]
    concs = [HA, A, H_conc, OH_conc]
    ax.bar(ions, concs, color=["red", "blue", "green", "purple"])
    ax.set_ylabel("농도 (mM)")
    ax.set_title("HA, A⁻, H⁺, OH⁻ 농도 변화")
    st.pyplot(fig)

st.write("---")

# 이온 모형 표시
st.subheader("이온 모형 (상대적 개수 표현)")

# 이온 개수를 시각적으로 표현하기 위해 농도에 비례한 개수의 점을 찍는다.
max_points = 100
HA_points = int(min(max_points, HA))
A_points = int(min(max_points, A))
H_points = int(min(max_points, H_conc))
OH_points = int(min(max_points, OH_conc))

# 이온 위치 (랜덤)
np.random.seed(42)
HA_x = np.random.rand(HA_points) * 0.25  # 0~0.25 구간
HA_y = np.random.rand(HA_points)

A_x = 0.25 + np.random.rand(A_points) * 0.25  # 0.25~0.5 구간
A_y = np.random.rand(A_points)

H_x = 0.5 + np.random.rand(H_points) * 0.25  # 0.5~0.75 구간
H_y = np.random.rand(H_points)

OH_x = 0.75 + np.random.rand(OH_points) * 0.25  # 0.75~1 구간
OH_y = np.random.rand(OH_points)

fig2, ax2 = plt.subplots(figsize=(6,3))
ax2.scatter(HA_x, HA_y, c='red', alpha=0.6, label='HA')
ax2.scatter(A_x, A_y, c='blue', alpha=0.6, label='A⁻')
ax2.scatter(H_x, H_y, c='green', alpha=0.6, label='H⁺')
ax2.scatter(OH_x, OH_y, c='purple', alpha=0.6, label='OH⁻')
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(0,1)
ax2.set_ylim(0,1)
ax2.set_title("이온 모형 (점의 개수 ~ 농도)")
ax2.legend()
st.pyplot(fig2)

st.write("""
**해석**:  
- **막대 그래프**는 최종 HA, A⁻, H⁺, OH⁻ 농도를 보여줍니다.  
- **이온 모형**은 각 이온 수를 점으로 나타내어 농도가 높을수록 더 많은 점이 나타납니다.  
- 산(HCl) 추가 시: A⁻는 감소하고 HA와 H⁺가 증가  
- 염기(NaOH) 추가 시: HA는 감소하고 A⁻와 OH⁻가 증가  
- 공통 이온(A⁻) 추가 시: 완충 영역 내에서 평형 이동으로 인해 pH 변화 최소화
""")
