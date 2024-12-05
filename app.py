# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# 페이지 기본 설정
st.set_page_config(page_title="나만의 주기율표", layout="wide")

# 데이터 불러오기
@st.cache
def load_data():
    data = pd.read_csv("elementdatavalues.csv")  # 원소 데이터 파일
    return data

data = load_data()

# 사이드바 설정
st.sidebar.title("설정")
selected_property = st.sidebar.selectbox(
    "속성 선택",
    ["Atomic_Weight", "Electronegativity", "Density", "Melting_Point", "Boiling_Point"]
)
selected_view = st.sidebar.radio(
    "보기 모드",
    ["데이터 보기", "속성 분석", "주기율표 시각화"]
)

# 제목
st.title("🧪 나만의 주기율표")

# 데이터 보기
if selected_view == "데이터 보기":
    st.subheader("원소 데이터셋")
    st.write("아래는 원소 데이터의 일부분입니다. 속성을 탐색하세요.")
    st.dataframe(data.head())
    st.write(f"전체 데이터 크기: {data.shape[0]}행, {data.shape[1]}열")

# 속성 분석
elif selected_view == "속성 분석":
    st.subheader("속성별 데이터 분석")
    st.write(f"선택한 속성: {selected_property}")

    # 기본 통계량
    st.write("📊 기본 통계량")
    st.write(data[selected_property].describe())

    # 속성의 히스토그램
    st.write("📈 히스토그램")
    fig, ax = plt.subplots()
    ax.hist(data[selected_property].dropna(), bins=20, color="skyblue", edgecolor="black")
    ax.set_title(f"Histogram of {selected_property}")
    ax.set_xlabel(selected_property)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # 속성의 원자 번호에 따른 변화
    st.write("📉 원자 번호에 따른 변화")
    fig = px.scatter(data, x="Atomic_Number", y=selected_property,
                     hover_name="Name", title=f"{selected_property} by Atomic Number")
    st.plotly_chart(fig)

# 주기율표 시각화
elif selected_view == "주기율표 시각화":
    st.subheader("주기율표 시각화")
    st.write(f"선택한 속성: {selected_property}")

    # 주기율표 시각화
    fig = px.scatter(data, x="Group", y="Period",
                     size=selected_property, color=selected_property,
                     hover_name="Name", title=f"Periodic Table Visualized by {selected_property}")
    st.plotly_chart(fig)

    # 사용자 정의 주기율표
    st.write("🎨 사용자 정의 주기율표")
    user_color = st.color_picker("배경 색상 선택", "#FFFFFF")
    st.markdown(f"<style>.main {{ background-color: {user_color}; }}</style>", unsafe_allow_html=True)

    # 내보내기 기능
    if st.button("주기율표 저장"):
        fig.write_image("custom_periodic_table.png")
        st.success("주기율표가 'custom_periodic_table.png'로 저장되었습니다!")

# Footer
st.sidebar.markdown("### © 2024 Streamlit Chemistry App")
