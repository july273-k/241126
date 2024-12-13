import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 헨더슨-하셀바흐 식: pH = pKa + log([A-]/[HA])
# 여기서는 아세트산/아세트산나트륨 완충용액을 예로 듦
# pKa(아세트산) ~ 4.76 가정
pKa = 4.76

st.title("완충용액 공통 이온 효과 시뮬레이션")

st.write("""
이 웹 앱은 아세트산(HA) - 아세트산나트륨(A⁻) 완충용액에 산(HCl)이나 염기(NaOH) 또는 염(아세트산나트륨)을 추가하여
공통 이온 효과를 직관적으로 확인하기 위한 시뮬레이터입니다.

- 초기 조건: [HA]와 [A⁻]를 특정 농도로 설정  
- 사용자가 산, 염기, 염을 추가함에 따라 새로운 평형 상태의 pH와 이온 농도를 계산  
- 헨더슨-하셀바흐 식을 이용해 pH를 산출  
- 공통 이온(A⁻) 추가에 따른 pH 변화 및 완충 용액의 완충 능력 확인
""")

# 초기 농도 설정 (단위: mM)
initial_HA = st.sidebar.slider("초기 HA 농도 (mM)", min_value=1.0, max_value=100.0, value=50.0)
initial_A = st.sidebar.slider("초기 A⁻ 농도 (mM)", min_value=1.0, max_value=100.0, value=50.0)

# 사용자 입력: 추가할 물질 및 양
add_species = st.sidebar.selectbox("추가할 물질 선택", ["None", "강산(HCl)", "강염기(NaOH)", "아세트산나트륨(NaA)"])
added_amount = st.sidebar.slider("추가량 (mM)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)

# 초기 상태: 
# HA, A-의 농도를 mM -> M로 바꾸거나 그대로 비율만 고려해도 무방하지만, 여기서는 mM 단위 유지
# pH 계산: pH = pKa + log([A-]/[HA])

HA = initial_HA
A = initial_A

# 물질 추가에 따른 평형 변화 고려
# 1) 강산(HCl) 추가: HCl은 H+를 기부, A-와 반응하여 HA를 생성
#    HCl 추가 => [H+] 증가 => 일부 A-가 HA로 전환
#    반응식: A- + H+ -> HA
if add_species == "강산(HCl)" and added_amount > 0:
    # 추가된 H+는 A-와 반응
    # 반응 전: HA, A-
    # 추가된 H+: added_amount
    # 반응 한도: min(A-, added_amount)
    delta = min(A, added_amount)
    A = A - delta
    HA = HA + delta
    # 남는 H+가 있을 수도 있으나, 여기서는 완충 영역 고려.
    # 남는 H+는 pH에 영향을 줄 것이나, 여기서는 완충용액 내에서 대부분 중화된다고 가정.
    # 실제로 남는 H+는 [H+] 직접 계산 필요.
    # 단순화: 남은 H+는 added_amount - delta, 이를 [H+] 증가로 반영
    # 실제 더 정확한 계산을 위해선 용액의 부피나 pkW 고려 필요
    leftover_H = added_amount - delta
    # leftover_H가 있으면 pH에 직접 영향
    # 여기서는 헨더슨-하셀바흐식에 잔류 H+ 반영 어려움으로 
    # 잔류 H+를 아주 작게나마 A-/HA 비에 반영해 근사
    # 다만, 간단화를 위해 leftover_H가 0이 아닐 경우, 그만큼 HA증가로 간주
    # (정확한 모델은 아니지만, 시연 목적)
    if leftover_H > 0:
        # leftover_H 만큼 HA 증가 가정
        HA += leftover_H

# 2) 강염기(NaOH) 추가: OH-는 HA와 반응하여 A-를 생성, H2O를 형성
#    HA + OH- -> A- + H2O
if add_species == "강염기(NaOH)" and added_amount > 0:
    delta = min(HA, added_amount)
    HA = HA - delta
    A = A + delta
    leftover_OH = added_amount - delta
    # leftover_OH가 남아있다면 강염기성으로 pH 큰 변동 가능
    # 여기서는 leftover_OH를 단순히 A- 증가로 반영하는 것은 적절치 않음
    # 실제로 leftover_OH는 용액의 pH를 크게 높임.
    # 간단히 leftover_OH만큼 A 증가(또는 별도 표시)로 처리 불가.
    # 정확한 해석을 위해선 [OH-] 직접 계산 필요하지만, 여기서는 간단화.
    if leftover_OH > 0:
        # 매우 강한 염기성으로 변하는 경우
        # 일단 A- 증가 없이 OH- 남긴 상태로 pH 계산을 단순화
        # pH 계산에 잔류 OH- 반영은 PKw=14 가정:
        # [OH-] = leftover_OH (mM) -> pOH = -log10([OH-]) -> pH = 14 - pOH
        # 단, 이 경우 A-/HA 비는 의미가 줄어듦. 완충 영역 벗어나는 상황.
        # 아래에서 조건부 처리
        pass

# 3) 아세트산나트륨(NaA) 추가: 이는 [A-]를 직접 증가시킴
if add_species == "아세트산나트륨(NaA)" and added_amount > 0:
    A = A + added_amount

# pH 계산
# 기본적으로 완충 영역 내에서는 헨더슨-하셀바흐 식 사용 가능
# 만약 강산/강염기 추가로 인해 완충 영역을 벗어났다면 근사적 계산 필요
# 여기서는 단순화: A-와 HA 농도가 둘 다 > 0이면 헨더슨-하셀바흐 사용
# 강염기 잔여분 leftover_OH, 강산 잔여분 leftover_H가 있으면 별도 처리

if add_species == "강염기(NaOH)" and added_amount > 0:
    # leftover_OH 계산
    leftover_OH = added_amount - min(HA+delta, added_amount)  # delta는 위에서 already accounted
    if leftover_OH > 0:
        # 용액이 매우 염기성일 경우: [OH-] = leftover_OH mM
        # mM -> M 변환 가정하지 않고 상대적 값만 사용 시,
        # 그냥 -log10( leftover_OH * 1e-3 ) 사용하는 것이 합리적일 것.
        # 여기서는 간단히 leftover_OH가 매우 작지 않다고 가정, pH계산:
        # pOH = -log10([OH-]) (M 단위 필요)
        # 가정: 1 mM = 1e-3 M
        OH_conc = leftover_OH * 1e-3
        pOH = -np.log10(OH_conc)
        pH = 14 - pOH
    else:
        # 완충 영역 내에 있다는 가정 하에 pH 계산
        if A > 0 and HA > 0:
            pH = pKa + np.log10(A/HA)
        else:
            # A나 HA 중 하나가 0이면 pH 극단 변동
            # HA=0이면 강염기성, A=0이면 강산성
            # 여기서는 단순화: A=0일 경우 pH≈0, HA=0일 경우 pH≈14 가정
            if A <= 0:
                pH = 0
            elif HA <= 0:
                pH = 14
else:
    # 강산 추가 경우 leftover_H 고려
    if add_species == "강산(HCl)" and added_amount > 0:
        leftover_H = added_amount - min(A+added_amount, added_amount)
        if leftover_H > 0:
            # 매우 산성인 경우 pH 계산
            H_conc = leftover_H * 1e-3
            pH = -np.log10(H_conc)
        else:
            # 완충 영역 내 헨더슨-하셀바흐
            if A > 0 and HA > 0:
                pH = pKa + np.log10(A/HA)
            else:
                if A <= 0:
                    pH = 0
                elif HA <= 0:
                    pH = 14
    else:
        # 공통 이온 추가만 되었거나 변화 없는 경우
        if A > 0 and HA > 0:
            pH = pKa + np.log10(A/HA)
        else:
            if A <= 0:
                pH = 0
            elif HA <= 0:
                pH = 14

st.subheader("결과")
st.write(f"최종 pH: {pH:.2f}")
st.write(f"최종 HA 농도: {HA:.2f} mM")
st.write(f"최종 A⁻ 농도: {A:.2f} mM")

# 이온 농도 시각화
fig, ax = plt.subplots(figsize=(6,4))
ions = ["HA", "A⁻"]
concs = [HA, A]
ax.bar(ions, concs, color=["red", "blue"])
ax.set_ylabel("농도 (mM)")
ax.set_title("HA와 A⁻ 농도 변화")
st.pyplot(fig)

st.write("""
**해석**:  
- 추가된 강산(HCl)은 A⁻를 HA로 전환하여 pH 하락을 유도하며, 그럼에도 완충 용액은 pH 변화를 완화합니다.  
- 강염기(NaOH)는 HA를 A⁻로 전환하여 pH를 상승시키고, 완충 영역을 벗어나면 용액은 매우 염기성으로 변합니다.  
- 공통 이온인 A⁻를 아세트산나트륨 형태로 추가하면, 평형이 HA->H+ + A⁻ 방향에서 HA로 가는 반응이 억제되어 pH 상승이 억제되거나 pH가 약간 변동하는 공통 이온 효과를 볼 수 있습니다.
""")
