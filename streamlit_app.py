import streamlit as st
from my_agent import extract_conditions, classify_games, write_recommendations, review_recommendations

st.title("🎮 게임 추천 에이전트")
st.write("조건을 입력하면 맞는 게임을 추천해드립니다!")

st.subheader("입력 조건")
genre = st.selectbox("장르", ["RPG", "액션", "시뮬레이션", "어드벤처", "FPS", "샌드박스"])
platform = st.selectbox("플랫폼", ["닌텐도", "PC", "콘솔", "모바일"])
difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움"])
player = st.selectbox("플레이어", ["싱글", "멀티"])

if st.button("추천받기"):
    input_text = f"""
장르: {genre}
플랫폼: {platform}
난이도: {difficulty}
플레이어: {player}
"""
    conditions = extract_conditions(input_text)
    matched = classify_games(conditions)
    result = write_recommendations(conditions, matched)
    review = review_recommendations(matched)

    st.subheader("추천 결과")
    st.markdown(result)

    st.subheader("검토 보고서")
    st.markdown(review)