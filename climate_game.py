import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random

# 초기 데이터 구성
if "player_data" not in st.session_state:
    st.session_state.player_data = pd.DataFrame({
        "도시": ["서울", "부산", "대구"],
        "위도": [37.5665, 35.1796, 35.8722],
        "경도": [126.9780, 129.0756, 128.6014],
        "환경 점수": [50, 45, 60],
        "경제 점수": [50, 60, 55],
        "사회 점수": [50, 55, 45],
        "인구": [1000000, 800000, 700000],
        "세금": [50000, 48000, 47000],
        "총 점수": [150, 160, 160]
    })

# 정책 데이터
POLICIES = {
    "탄소세 도입": {"환경": 15, "경제": -5, "사회": -3},
    "재생에너지 투자": {"환경": 10, "경제": -4, "사회": 2},
    "화석연료 보조금": {"환경": -10, "경제": 7, "사회": 5},
    "대중교통 확장": {"환경": 8, "경제": -3, "사회": 4},
    "산업 확장": {"환경": -8, "경제": 10, "사회": -4}
}

# 랜덤 이벤트 데이터
RANDOM_EVENTS = [
    {"설명": "대규모 산불로 숲이 파괴되었습니다.", "효과": {"환경": -10, "경제": 0, "사회": -2}},
    {"설명": "재생에너지 기술 혁신이 발생했습니다.", "효과": {"환경": 15, "경제": 5, "사회": 0}},
    {"설명": "경제 불황이 발생했습니다.", "효과": {"환경": 0, "경제": -10, "사회": -5}}
]

# 도시 추가 함수
def add_city(name, lat, lon):
    new_city = {
        "도시": name,
        "위도": lat,
        "경도": lon,
        "환경 점수": 50,
        "경제 점수": 50,
        "사회 점수": 50,
        "인구": 1000000,
        "세금": 50000,
        "총 점수": 150
    }
    st.session_state.player_data = st.session_state.player_data.append(new_city, ignore_index=True)

# 지도 생성 함수
def create_map(data):
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=[row["위도"], row["경도"]],
            radius=10,
            color="green" if row["총 점수"] > 150 else "red",
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['도시']}: 총 점수 {row['총 점수']}"
        ).add_to(m)
    return m

# Streamlit UI
st.title("기후 위기 도시 경쟁")
st.sidebar.header("도시 관리")

# 도시 추가
with st.sidebar.expander("도시 추가"):
    new_city = st.text_input("도시 이름")
    lat = st.number_input("위도", value=36.5, step=0.1)
    lon = st.number_input("경도", value=127.5, step=0.1)
    if st.button("도시 추가"):
        add_city(new_city, lat, lon)
        st.success(f"{new_city} 도시가 추가되었습니다!")

# 정책 선택 및 반영
st.subheader("도시 상태")
selected_city = st.selectbox("관리할 도시를 선택하세요", st.session_state.player_data["도시"])
city_data = st.session_state.player_data[st.session_state.player_data["도시"] == selected_city].iloc[0]
st.write(f"도시: {city_data['도시']}")
st.write(f"환경 점수: {city_data['환경 점수']}")
st.write(f"경제 점수: {city_data['경제 점수']}")
st.write(f"사회 점수: {city_data['사회 점수']}")
st.write(f"인구: {city_data['인구']}")
st.write(f"세금: {city_data['세금']}")

policy = st.radio("정책 선택", list(POLICIES.keys()))
if st.button("정책 적용"):
    effects = POLICIES[policy]
    idx = st.session_state.player_data[st.session_state.player_data["도시"] == selected_city].index[0]
    for key, value in effects.items():
        st.session_state.player_data.loc[idx, f"{key} 점수"] += value
    st.session_state.player_data.loc[idx, "총 점수"] = (
        st.session_state.player_data.loc[idx, "환경 점수"] +
        st.session_state.player_data.loc[idx, "경제 점수"] +
        st.session_state.player_data.loc[idx, "사회 점수"]
    )
    st.success(f"{policy} 정책이 적용되었습니다!")

# 랜덤 이벤트 적용
if st.button("랜덤 이벤트 발생"):
    event = random.choice(RANDOM_EVENTS)
    st.info(event["설명"])
    idx = st.session_state.player_data[st.session_state.player_data["도시"] == selected_city].index[0]
    for key, value in event["효과"].items():
        st.session_state.player_data.loc[idx, f"{key} 점수"] += value

# 리더보드
st.subheader("리더보드")
leaderboard = st.session_state.player_data.sort_values(by="총 점수", ascending=False)
st.table(leaderboard[["도시", "총 점수", "인구", "세금"]])

# 지도 시각화
st.subheader("도시 지도")
city_map = create_map(st.session_state.player_data)
folium_static(city_map)
