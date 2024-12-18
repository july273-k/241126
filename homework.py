import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import folium
from streamlit_folium import st_folium

#----------------------------------------------
# 데이터 준비 (샘플)
# 나이팅게일의 로즈 다이어그램 예시 데이터(사망원인별 월별 사망자 수)
# 실제 나이팅게일 데이터는 크림 전쟁 당시 병사 사망자 수(전투 관련, 질병 관련, 기타)를 12개월 간 기록한 것.
# 여기서는 간단한 가상 데이터 사용
data_rose = pd.DataFrame({
    'month': ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    'Disease': [120, 80, 50, 30, 20, 15, 10, 12, 25, 60, 90, 110],
    'Wounds': [30, 25, 20, 15, 10, 10, 12, 18, 20, 22, 28, 32],
    'Other': [10, 5, 5, 8, 8, 9, 10, 12, 15, 15, 12, 10]
})

# 존 스노우의 콜레라 지도: 
# 1854년 소호 지구의 펌프 위치 및 콜레라 사망자 위치 표시 (여기서는 예시 데이터)
pumps = pd.DataFrame({
    'name': ['Pump A', 'Pump B', 'Pump C'],
    'lat': [51.5134, 51.5123, 51.5130],
    'lon': [-0.1362, -0.1375, -0.1355]
})

cholera_deaths = pd.DataFrame({
    'lat': [51.5135, 51.5136, 51.5132, 51.5129, 51.5125, 51.5131],
    'lon': [-0.1361, -0.1363, -0.1360, -0.1370, -0.1372, -0.1359],
})


#----------------------------------------------
# 페이지 구성

st.title("데이터 시각화 체험 웹앱")
st.sidebar.title("메뉴")

page = st.sidebar.selectbox("페이지 선택", ["소개", "나이팅게일의 로즈 다이어그램", "존 스노우의 콜레라 지도"])


if page == "소개":
    st.header("데이터 시각화의 의의와 과학적 활용")
    st.write("""
    데이터 시각화는 단순한 숫자나 표 형태의 정보를 직관적으로 파악할 수 있도록 돕는 강력한 도구입니다.  
    역사적으로도 중요 현상이나 문제를 해결하기 위해 시각화를 활용한 사례가 있습니다.
    
    **사례 1: 플로렌스 나이팅게일(Florence Nightingale)**  
    나이팅게일은 크림 전쟁 당시 병사들의 사망 원인을 시각화한 '로즈 다이어그램(Rose Diagram)'을 통해, 질병에 의한 사망률 감소의 중요성을 강조하였습니다.
    
    **사례 2: 존 스노우(John Snow)**  
    1854년 런던 콜레라 유행 시기, 존 스노우는 콜레라 사망자 위치를 지도 위에 표시하여 특정 펌프에서 공급되는 물이 원인임을 밝혀냈습니다.
    
    이 앱에서는 위 두 사례를 데이터 시각화를 통해 체험해보고, 데이터 리터러시를 기르는 경험을 할 수 있습니다.
    """)

elif page == "나이팅게일의 로즈 다이어그램":
    st.header("나이팅게일의 로즈 다이어그램 체험")
    st.write("""
    아래는 월별 사망자 수를 원인별로 나타낸 샘플 데이터(가상)로 로즈 다이어그램을 구현한 예시입니다.
    각 월을 중심각으로 하여, 원인별 사망자수를 부채꼴 형태로 표현합니다.
    """)

    # 사용자 선택: 표시할 원인
    causes = ['Disease', 'Wounds', 'Other']
    selected_causes = st.multiselect("표시할 사망원인 선택", causes, default=causes)

    # 선택한 원인만 합산한 값으로 차트 생성
    data_rose['total'] = data_rose[selected_causes].sum(axis=1)

    # Altair 사용 Polar Chart 만들기
    base = alt.Chart(data_rose).mark_arc(innerRadius=20).encode(
        theta=alt.Theta("total:Q", stack=True),
        color=alt.Color("month:N", legend=None),
        tooltip=["month", "total"]
    )

    st.altair_chart(base, use_container_width=True)

    st.write("""
    위 그래프에서 색상은 월을 구분하며, 부채꼴의 크기는 해당 월의 사망자 수를 나타냅니다.  
    원인별 필터를 조정하며 시각화의 변화를 살펴보세요.
    """)

elif page == "존 스노우의 콜레라 지도":
    st.header("존 스노우의 콜레라 지도 체험")
    st.write("""
    아래 지도는 1854년 런던 소호 지역을 가상으로 단순화한 것이며, 파란색 마커는 펌프를, 빨간색 점은 콜레라 사망자 발생 위치를 의미합니다.
    존 스노우는 이러한 데이터를 지도 위에 표시함으로써 특정 펌프에서 공급되는 물과 콜레라 발생 간의 상관관계를 추론할 수 있었습니다.
    """)

    # 맵 생성
    map_center = [51.5130, -0.1365]
    m = folium.Map(location=map_center, zoom_start=17)

    # 펌프 표시
    for i, row in pumps.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=row['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # 콜레라 사망자 표시
    for i, row in cholera_deaths.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            fill=True,
            color='red',
            fill_opacity=0.7
        ).add_to(m)

    st_map = st_folium(m, width=700, height=500)

    st.write("""
    위 지도에서 '파란색 마커'는 펌프 위치를, '빨간색 점'은 콜레라 사망자 발생지를 나타냅니다.  
    존 스노우는 이러한 지도를 통해 특정 펌프 주변에 사망자가 집중됨을 알아냈고, 이를 기반으로 콜레라가 오염된 물로 인해 발생한다는 과학적 가설을 수립할 수 있었습니다.
    """)
