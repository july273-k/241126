import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header("2차시: 데이터를 통한 원소의 주기적 경향성 탐구")

try:
    elements = pd.read_csv("elements_data.csv")
    
    # 열 이름 변환
    elements.rename(columns={
        "AtomicNumber": "원소 번호",
        "AtomicMass": "원자량",
        "Density": "밀도",
        "MeltingPoint": "녹는점",
        "BoilingPoint": "끓는점",
        "AtomicRadius": "원자 반지름",
        "IonizationEnergy": "이온화 에너지",
        "Electronegativity": "전기 음성도"
    }, inplace=True)
    
    st.write("데이터 열 이름:", elements.columns.tolist())  # 열 이름 확인
    property_choice = st.selectbox("속성 선택", ["원자량", "밀도", "녹는점", "끓는점", "원자 반지름", "이온화 에너지", "전기 음성도"])
    
    # KeyError 방지
    if "원소 번호" in elements.columns and property_choice in elements.columns:
        fig, ax = plt.subplots()
        ax.plot(elements["원소 번호"], elements[property_choice])
        ax.set_title(f"{property_choice} 변화")
        ax.set_xlabel("원소 번호")
        ax.set_ylabel(property_choice)
        st.pyplot(fig)
    else:
        st.error("데이터에 필요한 열이 없습니다. CSV 파일을 확인하세요.")
except FileNotFoundError:
    st.error("CSV 파일 'elements_data.csv'을(를) 찾을 수 없습니다.")
