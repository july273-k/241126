import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
file_path = '/mnt/data/elements_data.csv'
elements = pd.read_csv(file_path)

# 메인 타이틀
st.title("데이터와 과학적 탐구를 통한 주기적 경향성 학습")

# 차시 선택
tab1, tab2, tab3, tab4 = st.tabs(["1차시: 데이터 시각화", "2차시: 주기적 경향성 탐구", "3차시: 경향성 설명", "4차시: CoSpaces 주기율표"])

# 1차시: 데이터 시각화
with tab1:
    st.header("1차시: 데이터 시각화의 의의와 과학적 활용 탐구")
    
    st.subheader("나이팅게일의 로즈 다이어그램")
    st.write("""
    1854년 크림 전쟁 당시 나이팅게일은 군 병원의 위생 상태를 개선하기 위해 로즈 다이어그램을 활용했습니다.
    이를 통해 사망 원인을 시각적으로 보여주어 위생 환경 개선에 기여했습니다.
    """)
    st.image("nightingale_rose_diagram.png", caption="나이팅게일의 로즈 다이어그램")
    
    st.subheader("존 스노우의 콜레라 지도")
    st.write("""
    존 스노우는 1854년 런던 콜레라 발생 당시, 환자 분포를 지도에 표시하여 감염원이 특정 펌프임을 밝혀냈습니다.
    """)
    st.image("john_snow_cholera_map.jpg", caption="존 스노우의 콜레라 지도")
    
    st.subheader("데이터 시각화 실습")
    st.write("아래 데이터를 사용하여 간단한 바 차트를 생성해보세요.")
    data = {"항목": ["A", "B", "C", "D"], "값": [23, 45, 56, 78]}
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("항목"))

# 2차시: 주기적 경향성 탐구
with tab2:
    st.header("2차시: 데이터를 통한 원소의 주기적 경향성 탐구")
    
    st.subheader("원소 데이터 시각화")
    st.write("아래 데이터를 활용하여 원소의 속성을 선택하고 그래프를 확인하세요.")
    
    property_choice = st.selectbox(
        "속성 선택", 
        ["Atomic_Weight", "Density", "Melting_Point", "Boiling_Point", "Atomic_Radius", "Electronegativity"]
    )
    
    fig, ax = plt.subplots()
    ax.plot(elements["Atomic_Number"], elements[property_choice])
    ax.set_title(f"{property_choice} 변화")
    ax.set_xlabel("Atomic Number (원소 번호)")
    ax.set_ylabel(property_choice)
    st.pyplot(fig)
    
    st.subheader("탐구 질문 생성")
    st.text_input("탐구 질문 예시: 원자 반지름은 왜 같은 족에서 증가하고, 같은 주기에서는 감소하는가?")

# 3차시: 원소 주기적 경향성 설명
with tab3:
    st.header("3차시: 원소의 주기적 경향성 과학적 개념으로 설명하기")
    
    st.subheader("탐구 질문에 대한 과학적 설명")
    st.write("전자 배치, 핵 전하, 가리움 효과 등을 활용하여 질문을 설명하세요.")
    st.text_area("탐구 결과 공유", placeholder="탐구 질문에 대한 설명을 작성하세요.")
    
    st.subheader("데이터 기반 결론 도출")
    st.write("1, 2차시에서 학습한 내용을 바탕으로 데이터를 활용해 결론을 도출하세요.")

# 4차시: CoSpaces 활용한 주기율표 제작
with tab4:
    st.header("4차시: CoSpaces 활용한 나만의 주기율표 제작")
    
    st.subheader("CoSpaces 사용 안내")
    st.write("""
    CoSpaces를 활용하여 창의적이고 상호작용적인 3D 주기율표를 제작하세요.
    CoBlocks를 사용하여 원소 정보를 반영한 상호작용 요소를 추가하세요.
    """)
    
    st.subheader("주기율표 설계 아이디어")
    st.text_area("설계 아이디어 작성", placeholder="예: 전기 음성도에 따라 색상을 구분한 3D 주기율표 설계")
    
    st.subheader("작업 결과 공유")
    st.text_area("발표 내용 작성", placeholder="작업 과정 및 결과 발표 내용을 작성하세요.")
